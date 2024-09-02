# Function to test if a directory exists and create it if it does not
function Test-Directory {
    param (
        [string]$DirPath  # Parameter to accept the directory path
    )
    # Test If Directory Exists, Create If It Does Not
    if (-not (Test-Path $DirPath)) {
        New-Item -ItemType Directory -Path $DirPath -Force  # Create the directory
    }
}

# Function to remove all files from a specified location
function Remove-TempFiles {
    param (
        [string]$RemoveLoc  # Parameter to accept the location from which files will be removed
    )
    # Remove Files From Temporary Folder
    Get-ChildItem -Path $RemoveLoc -File | Remove-Item -Force  # Get all files and remove them
}

# Function to expand a LZMA compressed file using 7-Zip
function Expand-LZMA {
    param (
        [string]$InputPath,  # Parameter to accept the input file path
        [string]$OutputPath  # Parameter to accept the output directory path
    )
    # Check if the input file exists
    if (-not (Test-Path $InputPath)) {
        Write-Host "The input file does not exist."  # Output message if file does not exist
        exit  # Exit the function
    }

    # Decompress the file using 7z
    try {
        $7zPath = "${env:ProgramFiles}\7-Zip\7z.exe"  # Path to the 7-Zip executable
        & $7zPath x $InputPath "-o$OutputPath" -y | Out-Null  # Execute 7-Zip to decompress the file
    } catch {
        Write-Host "An error occurred during decompression."  # Output message if an error occurs
    }
}