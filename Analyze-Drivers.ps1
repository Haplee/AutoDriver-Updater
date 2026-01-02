<#
.SYNOPSIS
    Analyzes the system's drivers to identify potential issues.

.DESCRIPTION
    This PowerShell script queries the state of all installed drivers on a Windows system.
    It identifies drivers that are currently stopped or are not digitally signed and
    compiles the findings into a user-friendly text report.

    This script requires administrative privileges to run.

.AUTHOR
    Jules - AI Software Engineer

.DATE
    2023-10-27
#>

#Requires -RunAsAdministrator

# --- SCRIPT CONFIGURATION ---
$ReportFile = "Driver-Report.txt"
$ProgressPreference = 'SilentlyContinue' # Suppress progress bars from cmdlets

# --- SCRIPT BODY ---

# 1. Check for Administrator Privileges
Write-Host "Verifying administrator privileges..."
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script must be run with Administrator privileges. Please right-click the script and select 'Run as Administrator'."
    # Pause to allow the user to read the error before the window closes
    Start-Sleep -Seconds 10
    Exit 1
}
Write-Host "Administrator privileges confirmed." -ForegroundColor Green

# 2. Execute Driver Queries and Convert to Objects
Write-Host "Querying system drivers... (This may take a moment)"
try {
    # Using CSV format for easy and reliable object conversion in any language
    $allDrivers = driverquery /v /fo csv | ConvertFrom-Csv
    $signedDriversInfo = driverquery /si /fo csv | ConvertFrom-Csv
}
catch {
    Write-Error "Failed to execute 'driverquery'. Please ensure the command is available in your system's PATH."
    Start-Sleep -Seconds 10
    Exit 1
}

Write-Host "Driver query complete. Analyzing data..."

# 3. Analyze the Driver Data
$stoppedDrivers = $allDrivers | Where-Object { $_.State -eq 'Stopped' }
$unsignedDrivers = $signedDriversInfo | Where-Object { $_.IsSigned -eq 'False' }

# 4. Generate the Report
Write-Host "Generating report file: $ReportFile"

# Report Header
$reportContent = @"
=================================
  Driver Analysis Report
=================================
Generated on: $(Get-Date)

--- SUMMARY ---
This report identifies drivers that are currently stopped or not digitally signed.
While this information can be useful for troubleshooting, please note that not every
item listed necessarily indicates a problem.

- Stopped Drivers Found: $($stoppedDrivers.Count)
- Unsigned Drivers Found: $($unsignedDrivers.Count)

"@

# Stopped Drivers Section
$reportContent += @"

--- STOPPED DRIVERS ---
Drivers that are not currently running. This can be normal for drivers that are
loaded on demand. However, if a critical device is not working, its driver
might be listed here.

"@

if ($stoppedDrivers) {
    foreach ($driver in $stoppedDrivers) {
        $reportContent += @"
- Display Name: $($driver.'Display Name')
  Service Name: $($driver.'Module Name')
  State:          $($driver.State)
  PnP Device ID:  $($driver.'PnP Device ID')

"@
    }
}
else {
    $reportContent += "No stopped drivers found.`n"
}

# Unsigned Drivers Section
$reportContent += @"

--- UNSIGNED DRIVERS ---
Drivers that do not have a digital signature from Microsoft. Unsigned drivers
can sometimes cause system instability. It is important to verify their origin.

"@

if ($unsignedDrivers) {
    foreach ($driver in $unsignedDrivers) {
        $reportContent += @"
- Device Name: $($driver.'Device Name')
  Signed:      $($driver.IsSigned)
  Driver Version: $($driver.'Driver Version')

"@
    }
}
else {
    $reportContent += "No unsigned drivers found.`n"
}

# Recommendations Footer
$reportContent += @"

--- RECOMMENDATIONS ---
1. Windows Update: Always check Windows Update first for official drivers.
2. Manufacturer's Website: For hardware like graphics cards or motherboards,
   download drivers directly from the manufacturer's official website (e.g.,
   NVIDIA, AMD, Intel, Dell, HP).
3. AVOID third-party driver download websites. They can bundle unwanted software
   or provide incorrect drivers.

This tool is a supplement to, not a replacement for, Windows Update.
"@

# Write the report to a file
try {
    Set-Content -Path $ReportFile -Value $reportContent -Encoding UTF8
    Write-Host "Report successfully saved to $(Resolve-Path $ReportFile)." -ForegroundColor Green
}
catch {
    Write-Error "Failed to write the report file. Error: $_"
    Start-Sleep -Seconds 10
    Exit 1
}

Write-Host "Analysis complete."
# Pause at the end for visibility when run directly
Start-Sleep -Seconds 5
