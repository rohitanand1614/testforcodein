Write-Host "Starting wait_until_6am job..."

# Define the IST timezone
$ISTTimeZone = [System.TimeZoneInfo]::FindSystemTimeZoneById("India Standard Time")

# Infinite loop to check the time
while ($true) {
    # Get the current system time (local time)
    $localTime = Get-Date

    # Convert the local time to IST
    $ISTTime = [System.TimeZoneInfo]::ConvertTime($localTime, $ISTTimeZone)

    # Format the IST time to HH:mm for comparison
    $currentISTTime = $ISTTime.ToString("HH:mm")

    # Check if the IST time is 6:00 AM
    if ($currentISTTime -eq "06:00") {
        Write-Host "It's 6 AM IST! Proceeding to execute pipeline..."
        break
    } else {
        Write-Host "Current IST time: $currentISTTime. Waiting until 6 AM IST..."
        Start-Sleep -Seconds 60  # Sleep for 60 seconds before checking again
    }
}

# Simulate the execution pipeline
Write-Host "Pipeline execution started at $(Get-Date)"
