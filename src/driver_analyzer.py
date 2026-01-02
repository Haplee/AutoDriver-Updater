# -*- coding: utf-8 -*-

"""
Driver Analyzer for Windows.

This script analyzes the state of system drivers using native Windows commands,
identifies potential issues, and generates a summary report.
"""

import os
import subprocess
import ctypes
import sys
from datetime import datetime
import webbrowser
import pathlib

def open_web_page():
    """Opens the local web/index.html page in the default browser."""
    try:
        # Determine the base path, works for script and frozen exe
        if getattr(sys, 'frozen', False):
            # The executable is running from a temporary directory, but we need the path where it's stored
            base_path = pathlib.Path(sys.executable).parent
        else:
            # Running as a script, go up from src/ to the project root
            base_path = pathlib.Path(__file__).parent.parent

        web_file_path = base_path / 'web' / 'index.html'

        if web_file_path.exists():
            print(f"Opening help page from: {web_file_path.resolve()}")
            webbrowser.open(f'file://{web_file_path.resolve()}')
        else:
            print(f"Error: Could not find the help file at '{web_file_path}'.")
            print("Please ensure the 'web' folder is in the same directory as the executable.")
    except Exception as e:
        print(f"An error occurred while trying to open the web page: {e}")

def is_admin():
    """Checks if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(command):
    """Executes a system command and returns its output, handling potential errors."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='cp850',
            errors='ignore'
        )
        return result.stdout
    except FileNotFoundError:
        print(f"Error: The command '{command[0]}' was not found. Make sure it is in the system's PATH.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Error output (stderr):\n{e.stderr}")
        return None

def parse_driver_v_output(output):
    """
    Parses the detailed output from 'driverquery /v /fo list'.
    Handles both English and Spanish headers by normalizing them.
    """
    drivers = []
    if not output:
        return drivers

    # Normalize headers from Spanish to a common key format
    header_map = {
        'Nombre de módulo': 'ModuleName', 'Module Name': 'ModuleName',
        'Nombre a mostrar': 'DisplayName', 'Display Name': 'DisplayName',
        'Descripción del controlador': 'Description', 'Driver Description': 'Description',
        'Tipo de controlador': 'Driver Type', 'Tipo': 'Driver Type',
        'Estado': 'State',
        'PnP Device ID': 'PnPDeviceID',
    }

    records = output.strip().split('\n\n')
    for record in records:
        driver = {}
        lines = record.strip().split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                # Use the mapped key if it exists, otherwise use the original
                normalized_key = header_map.get(key, key)
                driver[normalized_key] = value.strip()
        if driver:
            drivers.append(driver)

    return drivers

def parse_signed_driver_output(output):
    """
    Parses the CSV output from 'driverquery /si' to find unsigned drivers.
    This function is language-agnostic by finding the signature column by its header.
    """
    unsigned_drivers = []
    if not output:
        return unsigned_drivers

    lines = output.strip().split('\n')
    if len(lines) < 2:
        return unsigned_drivers # No header or no data

    # Clean up and find the index of the signature status column
    header = [h.strip().replace('"', '') for h in lines[0].split(',')]

    # Headers can be 'IsSigned' (English) or 'Está firmado' (Spanish)
    is_signed_index = -1
    if 'IsSigned' in header:
        is_signed_index = header.index('IsSigned')
    elif 'Está firmado' in header:
        is_signed_index = header.index('Está firmado')

    if is_signed_index == -1:
        print("Warning: Could not determine the signature status column in 'driverquery /si' output.")
        # Fallback for safety, though it might be incorrect.
        if len(header) > 1: is_signed_index = 1
        else: return unsigned_drivers

    # The device name is reliably the first column
    device_name_index = 0

    # Process the data rows
    for line in lines[1:]:
        if line.strip():
            parts = [p.strip().replace('"', '') for p in line.split(',')]
            if len(parts) > is_signed_index:
                signature_status = parts[is_signed_index].lower()
                if signature_status == 'false':
                    device_name = parts[device_name_index]
                    unsigned_drivers.append(device_name)

    return unsigned_drivers

def generate_report(stopped_drivers, unsigned_drivers):
    """Generates a report.txt file with the analysis results."""
    report_path = "report.txt"
    print(f"Generating report at: {os.path.abspath(report_path)}")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Driver Analysis Report\n")
        f.write("======================\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("--- Summary ---\n")
        f.write(f"Found {len(stopped_drivers)} stopped drivers.\n")
        f.write(f"Found {len(unsigned_drivers)} unsigned drivers.\n")
        f.write("Note: Not all stopped or unsigned drivers indicate a problem. This report is for informational purposes.\n\n")

        if stopped_drivers:
            f.write("--- Stopped Drivers ---\n")
            for driver in stopped_drivers:
                # Use the normalized keys to fetch data
                name = driver.get('ModuleName', 'N/A')
                display_name = driver.get('DisplayName', 'N/A')
                pnp_id = driver.get('PnPDeviceID', 'N/A')
                f.write(f"  - Name: {name}\n")
                f.write(f"    Display Name: {display_name}\n")
                f.write(f"    PnP Device ID: {pnp_id}\n\n")
        else:
            f.write("--- Stopped Drivers ---\n")
            f.write("No stopped drivers found.\n\n")

        if unsigned_drivers:
            f.write("--- Unsigned Drivers ---\n")
            for driver_name in unsigned_drivers:
                f.write(f"  - {driver_name}\n")
            f.write("\n")
        else:
            f.write("--- Unsigned Drivers ---\n")
            f.write("No unsigned drivers found.\n\n")

        f.write("--- Recommendations ---\n")
        f.write("1. Check Windows Update for the latest official drivers.\n")
        f.write("2. For specific hardware (e.g., graphics cards), visit the manufacturer's official website (NVIDIA, AMD, Intel).\n")
        f.write("3. Do NOT download drivers from third-party websites.\n")

def main():
    """
    Main function to orchestrate the driver analysis.
    Handles command-line arguments.
    """
    # Check for --view-web argument first
    if len(sys.argv) > 1 and sys.argv[1].lower() == '--view-web':
        open_web_page()
        sys.exit(0)

    if not is_admin():
        print("Error: This script requires administrative privileges.")
        print("Please run it as an administrator.")
        sys.exit(1)

    print("Starting driver analysis... This may take a moment.")

    print("Executing 'driverquery /v' to get detailed driver info...")
    driver_v_output = run_command(["driverquery", "/v", "/fo", "list"])

    print("Executing 'driverquery /si' to check for unsigned drivers...")
    signed_driver_output = run_command(["driverquery", "/si", "/fo", "csv"])

    if not driver_v_output and not signed_driver_output:
        print("Could not retrieve driver information. Exiting.")
        return

    print("Parsing driver information...")
    all_drivers = parse_driver_v_output(driver_v_output)
    unsigned_drivers = parse_signed_driver_output(signed_driver_output)

    stopped_drivers = [d for d in all_drivers if d.get('State', '').lower() == 'stopped']

    print("Generating report...")
    generate_report(stopped_drivers, unsigned_drivers)

    print("\n--- Analysis Complete ---")
    print(f"Found {len(stopped_drivers)} stopped drivers.")
    print(f"Found {len(unsigned_drivers)} unsigned drivers.")
    print(f"A detailed report has been saved to 'report.txt'.")

if __name__ == "__main__":
    main()
