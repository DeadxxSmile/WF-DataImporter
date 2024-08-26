# Load the file containing the functions used in this script 
. "$($PSScriptRoot)\bin\WFDI-Functions.ps1"

# Define the JSON file path
$jsonFilePath = "E:\OneDrive\Coding\Languages\Powershell\Projects\WF-DataImporter\JSON\2024-08-04\ExportWeapons_en_Cleaned.json"

# Load the JSON content
$jsonContent = Get-Content -Path $jsonFilePath -Raw | ConvertFrom-Json

# Access the ExportWeapons array
$weaponsArray = $jsonContent.ExportWeapons

# Prepare the output array
$weaponData = [System.Collections.ArrayList] @()

# Loop through each entry in the ExportWeapons array
foreach ($entry in $weaponsArray) {
    # Create a hashtable to store the values for this entry
    $weaponData.Add( [PSCustomObject]@{
        Weapon    = $entry.name
		DMG  = $entry.totalDamage
		IMPACT    = $entry.damagePerShot[0]
		PUNC  = $entry.damagePerShot[1]
		SLASH     = $entry.damagePerShot[2]
		HEAT      = $entry.damagePerShot[3]
		COLD     = $entry.damagePerShot[4]
		ELEC  = $entry.damagePerShot[5]
		TOXIN	  = $entry.damagePerShot[6]
		BLAST	  = $entry.damagePerShot[7]
		RAD = $entry.damagePerShot[8]
		GAS       = $entry.damagePerShot[9]
		MAG  = $entry.damagePerShot[10]
		VIRAL     = $entry.damagePerShot[11]
		CORR = $entry.damagePerShot[12]
		VOID      = $entry.damagePerShot[13]
		CRITCHAN  = $entry.criticalChance
		CRITMULTI = $entry.criticalMultiplier
		STATCHAN  = $entry.procChance
		FIRERATE  = $entry.fireRate
		MULTI = $entry.multishot
    })
}

# Define the CSV file path
$csvDir = Join-Path -Path $PSScriptRoot -ChildPath "CSV"
$csvFileDir = Join-Path -Path $csvDir -ChildPath (Get-Date).ToString("yyyy-MM-dd")
Test-Directory -DirPath $csvFileDir
$csvFilePath = Join-Path $csvFileDir -ChildPath "ExportWeapons_en.csv"

# Export the output to a CSV file
$weaponData | Export-Csv -Path $csvFilePath -NoTypeInformation

Write-Host "Data exported to $csvFilePath successfully."
