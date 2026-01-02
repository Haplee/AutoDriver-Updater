# PowerShell Driver Analysis Script

A simple and safe PowerShell script to analyze Windows drivers and identify potential issues.

This script uses the native `driverquery` command to gather information about installed drivers, focusing on those that are stopped or unsigned. It then generates a clean, readable text report named `Driver-Report.txt`.

This tool is a supplement to, not a replacement for, Windows Update.

## Features

-   **Clean and Simple**: A single, well-structured PowerShell script.
-   **Administrator Check**: Automatically verifies if it's running with the required admin privileges.
-   **Robust Parsing**: Uses PowerShell's native CSV conversion for reliable, language-agnostic driver analysis.
-   **Detailed Report**: Creates `Driver-Report.txt` with a summary of stopped and unsigned drivers, along with safe recommendations.
-   **Read-Only**: The script does not modify any system files or settings.

## How to Use

### 1. Adjust Execution Policy (One-time setup)

By default, Windows prevents the execution of PowerShell scripts. To run this script, you may need to change the execution policy for your user account.

1.  Open PowerShell (you can search for it in the Start Menu).
2.  Run the following command to allow scripts to run for your user account only:
    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```
3.  When prompted, press `Y` and then `Enter` to confirm.

### 2. Run the Script

1.  Download the `Analyze-Drivers.ps1` script to your computer.
2.  Right-click the `Analyze-Drivers.ps1` file.
3.  Select **Run with PowerShell**. Windows will prompt you for administrator permissions.
4.  The script will open a PowerShell window, perform the analysis, and display its progress.
5.  Once complete, the window will close automatically after a few seconds.
6.  A file named `Driver-Report.txt` will be created in the same folder where you saved the script.

## Disclaimer

This script is provided "as is" without any warranty. Use it at your own risk. The author is not responsible for any damage that may result from its use.
