function Test-Directory {
    param (
        [string]$DirPath
    )
    # Test If Directory Exists, Create If It Does Not
    if (-not (Test-Path $DirPath)) {
        New-Item -ItemType Directory -Path $DirPath -Force
    }
}
function Remove-TempFiles {
    param (
        [string]$RemoveLoc
    )
    # Remove Files From Temporary Folder
    Get-ChildItem -Path $RemoveLoc -File | Remove-Item -Force
}
function Expand-LZMA {
    param (
        [string]$InputPath,
        [string]$OutputPath
    )
    # Check if the input file exists
    if (-not (Test-Path $InputPath)) {
        Write-Host "The input file does not exist."
        exit
    }

    # Decompress the file using 7z
    try {
        $7zPath = "${env:ProgramFiles}\7-Zip\7z.exe"
        & $7zPath x $InputPath "-o$OutputPath" -y | Out-Null
        Write-Host "File decompressed successfully and saved to $OutputPath"
    }
    catch {
        Write-Host "An error occurred during decompression: $_"
    }
}

function Get-WFData {
    param (
        [string]$DownloadPath,
        [string]$CurrentKey,
        [string]$DataLink
    )
    # Set Key File Information
    $KeyFile = Join-Path -Path $CurrentKey -ChildPath "index_en.txt"
    $KeyData = Get-Content -Path $KeyFile

    foreach ($KeyName in $KeyData) {
        $CurrentURL = $DataLink + $KeyName
        $CurrentFile = $KeyName.Split("!")
        $CurrentPath = Join-Path -Path $DownloadPath -ChildPath $CurrentFile[0]
        try {
            Invoke-WebRequest $CurrentURL -OutFile $CurrentPath
        }
        catch {
            Write-Host "Failed to download $($CurrentURL): $_"
        }
    }
}

function Repair-JSON {
    param (
        [string]$JSONFolderPath,
        [string]$JSONCleanedFolder
    )
    # Get All JSON Files In Set Folder
    $JSONFiles = Get-ChildItem -Path $JSONFolderPath -Filter *.json -Name

    foreach ($JSONFile in $JSONFiles) {
        # Get Current JSON File Path
        $JSONFilePath = Join-Path -Path $JSONFolderPath -ChildPath $JSONFile

        # Set Cleaned JSON File Path
        $FileNameParts = $JSONFile.Split(".")
        $JSONCleanedPath = Join-Path -Path $JSONCleanedFolder -ChildPath ($FileNameParts[0] + "_Cleaned." + $FileNameParts[1])
    
        # Clean JSON File Of Any New Lines Before/After '\r' Carriage Return
        $JSONContent = Get-Content -Raw -Path $JSONFilePath
        $JSONCleaned = $JSONContent -replace '\s*\\r\s*', '\r'
    
        # Export Cleaned JSON To New Folder With '_Cleaned' Added To Filename
        Set-Content -Path $JSONCleanedPath -Value $JSONCleaned
    }
}