# Load the file containing the functions used in this script 
. "$($PSScriptRoot)\bin\WFDI-Functions.ps1"

# Set Folder Paths
$TempFolder = Join-Path -Path $PSScriptRoot -ChildPath "temp"
$KeyDir = Join-Path -Path $PSScriptRoot -ChildPath "Keys"
$WFDataDir = Join-Path -Path $PSScriptRoot -ChildPath "JSON"

# Set Save Locations For Key & JSON Files
$KeySavePath = Join-Path -Path $KeyDir -ChildPath (Get-Date).ToString("yyyy-MM-dd")
Test-Directory -DirPath $KeySavePath
$WFDataPath = Join-Path -Path $WFDataDir -ChildPath (Get-Date).ToString("yyyy-MM-dd")
Test-Directory -DirPath $WFDataPath

# Set URLs For Warframe Data & Key Download Filename
$KeyURL = "https://origin.warframe.com/PublicExport/index_en.txt.lzma"
$WFDataURL = "http://content.warframe.com/PublicExport/Manifest/"
$KeyDownload = Join-Path -Path $TempFolder -ChildPath "index_en.txt.lzma"

try {
    # Get The Current Key File And Save To Temp Folder
    Invoke-WebRequest $KeyURL -OutFile $KeyDownload

    # Expand The LZMA Archive And Save To Keys Folder
    Expand-LZMA -InputPath $KeyDownload -OutputPath $KeySavePath

    # Download Warframe Data Files To Temp Folder
    Get-WFData -DownloadPath $TempFolder -CurrentKey $KeySavePath -DataLink $WFDataURL

    # Fix Issues With Warframe JSON Files And Export To JSON Folder
    Repair-JSON -JSONFolderPath $TempFolder -JSONCleanedFolder $WFDataPath
}
catch {
    # Output Error Message
    Write-Host "Main Code Try/Catch Block - An error occurred: $_"
}
finally {
    # Clean Temporary Files Out Of Temp Folder
    Remove-TempFiles -RemoveLoc $TempFolder
}