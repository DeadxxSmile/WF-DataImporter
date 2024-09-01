# Warframe Data Importer
This Python script will download the most recent Public Export from the Digital Extremes servers. The script relies on 7zip at this time as the standard libraires for decrypting the index file do not work due to an issue with how DE is doing the compression. 

# How To Use
The script currently only works with the English language files. If anyone else wants to use this script I can modify it to also work with other languages. Simply run the 'WF-DataImporter.py' file and the script will do the rest. 

## Dependencies
The script requires a few dependencies to run at this time. Make sure you have these installed to run the script.
```
LZMA Archive
```
Currently none of the libraires I have found can decompress the LZMA file we have to first download from DE; there seems to be some kind of issue with how they have compressed the file and as such every library from all the languages I have tried will simply fail. But thankfully 7zip is a free option with a command line interface to allow us to still get at the needed files inside. 

As such the script is currently designed to be run on a Windows machine with 7zip installed in the standard location. If you are running on another OS, or have the program installed in another location you will need to modify the 'seven_zip_path' variable in the 'expand_lzma' function to work with your system.

```
requests
```
We use the 'requests' module in this script, so you need to make sure your copy of Python has access to it. For most normal installs of Python, simply run the command:

```
python -m pip install --upgrade requests
```
Modify the command to match your system or whatever python package manager you use.

## Directories
```
\temp
```
The script does not permanently save the LZMA archive, and also does some fixes to the JSON files (detailed later) and as such uses a temporary directory to house the initial downloads before expanding the archive and fixing the files. 

```
\Keys
```
Warframe's public export uses a file has at the end of the file names for the URL, and these are stored in an 'index_<language>.txt' file. The current file is stored in this directory. 

```
\JSON
```
This is where the script exports the downloaded JSON files and inside you will see a 'Public' and 'Custom' folder. The 'Public' folder contains the export from DE's servers, and the 'Custom' folder are JSON files we have made using data scrapped from locations like the Warframe Wiki. You will notice a '_Cleaned' added to the end of the files. The JSON files come very broken from DE, including extra new lines where there shouldn't be, and a duplicate 'masteryReq' field in the Weapons file. The script cleans up these issues as well as removes those duplicate entries before exporting the JSON files to this folder. 

# License
Distributed under the GNU GPL-3.0 license; please check the 'LICENSE' file in the GitHub repository for more information. 

# Disclaimer 
The following is the disclaimer that applies to all scripts, functions, one-liners, etc. This disclaimer supersedes any disclaimer included in any script, function, one-liner, etc.

You running this script/function means you will not blame the author(s) if this breaks your stuff. This script/function is provided AS IS without warranty of any kind. Author(s) disclaims all implied warranties including, without limitation, any implied warranties of merchantability or of fitness for a particular purpose. The entire risk arising out of the use or performance of the sample scripts and documentation remains with you. In no event shall author(s) be held liable for any damages whatsoever (including, without limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or inability to use the script or documentation. Neither this script/function, nor any part of it other than those parts that are explicitly copied from others, may be republished without author(s) express written permission. The author(s) retain the right to alter this disclaimer at any time. For the most up to date version of the disclaimer, see https://ucunleashed.com/code-disclaimer.


