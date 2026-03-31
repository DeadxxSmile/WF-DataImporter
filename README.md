# Warframe Data Importer

This Python script will download the most recent Public Export from the Digital Extremes servers.

The Python version of this script **no longer requires 7zip**, as it now uses Python’s built-in LZMA handling with a fallback method to correctly process DE’s compressed index file.

A PowerShell version of this script is also included, which **still relies on 7zip**, and functions the same way the original version of this project did.

---

# How To Use

The script currently only works with the English language files. If anyone else wants to use this script I can modify it to also work with other languages.

Simply run:

```bash
python WF-DataImporter.py
```

and the script will do the rest.

If you prefer not to use Python, you can instead run the PowerShell version located in:

```
\WFDI-PowerShell
```

---

## Dependencies

### Python Version (Recommended)

The Python version no longer requires 7zip.

It uses Python’s built-in `lzma` module, along with a fallback recovery method to handle the way Digital Extremes compresses their index file (which does not strictly follow standard end-of-stream formatting).

#### Required Modules

We use the `requests` module in this script, so you need to make sure your copy of Python has access to it.

For most normal installs of Python, simply run:

```bash
python -m pip install --upgrade requests
```

Modify the command to match your system or whatever Python package manager you use.

---

### PowerShell Version (Legacy / Alternative)

The PowerShell version still requires 7zip.

#### LZMA Archive (PowerShell Only)

The original implementation relies on 7zip because most standard libraries fail to decompress the LZMA file due to how DE compresses it.

As such, the PowerShell script is designed to run on a Windows machine with 7zip installed in the standard location.

If you are running on another OS, or have 7zip installed in a different location, you will need to modify the path inside the PowerShell script.

---

## Directories

### `\temp`

The script does not permanently save the LZMA archive, and also does some fixes to the JSON files (detailed later). Because of this, it uses a temporary directory to handle downloads and processing before exporting the final data.

---

### `\Keys`

Warframe's public export uses a hash at the end of file names for the URL. These are stored in an `index_<language>.txt` file.

The script downloads and stores this file in this directory.

---

### `\JSON`

This is where the script exports the downloaded JSON files.

Inside you will see:

- `Public` → Raw export from DE’s servers  
- `Custom` → Additional JSON files created from external sources (like the Warframe Wiki)

You will notice a `_Cleaned` suffix added to some files. The JSON files from DE can contain formatting issues such as:

- Extra new lines  
- Duplicate fields (such as `masteryReq` in the Weapons file)

The script automatically cleans these issues before saving the final output.

---

### `\WFDI-PowerShell`

This is the original version of the script that runs via PowerShell instead of Python.

If you don't want to install Python or deal with modules, you can use this version instead, but it still requires 7zip.

---

# License

Distributed under the GNU GPL-3.0 license; please check the `LICENSE` file in the GitHub repository for more information.

---

# Disclaimer

The following is the disclaimer that applies to all scripts, functions, one-liners, etc. This disclaimer supersedes any disclaimer included in any script, function, one-liner, etc.

You running this script/function means you will not blame the author(s) if this breaks your stuff. This script/function is provided **AS IS** without warranty of any kind. Author(s) disclaim all implied warranties including, without limitation, any implied warranties of merchantability or of fitness for a particular purpose.

The entire risk arising out of the use or performance of the sample scripts and documentation remains with you.

In no event shall author(s) be held liable for any damages whatsoever (including, without limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or inability to use the script or documentation.

Neither this script/function, nor any part of it other than those parts that are explicitly copied from others, may be republished without author(s) express written permission.

The author(s) retain the right to alter this disclaimer at any time.

For the most up to date version of the disclaimer, see:  
https://ucunleashed.com/code-disclaimer
