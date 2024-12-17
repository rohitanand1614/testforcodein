# Define the root folder where you want to search for Python files
$rootFolder = "C:\path\to\your\folder"

# Define the keyword you are looking for
$keyword = "your_keyword"

# Define the import statement you want to add
$importStatement = "import your_module"

# Get all .py files recursively
Get-ChildItem -Path $rootFolder -Filter *.py -Recurse | ForEach-Object {
    $filePath = $_.FullName
    
    # Read the file content into memory
    $fileContent = Get-Content -Path $filePath
    
    # Check if the keyword is present
    $keywordFound = $fileContent -match $keyword
    
    # Check if the import statement is present
    $importFound = $fileContent -match ("^" + [regex]::Escape($importStatement) + "$")

    # If keyword is present and import statement is not found
    if ($keywordFound -and -not $importFound) {
        
        # Create the new file content by adding the import statement at the top,
        # followed by a newline, then the original content.
        # Join the original content with newlines to ensure correct formatting.
        $newContent = $importStatement + [Environment]::NewLine + ($fileContent -join [Environment]::NewLine)
        
        # Write the updated content back to the file
        Set-Content -Path $filePath -Value $newContent
        Write-Host "Added import statement to $filePath"
    }
}
