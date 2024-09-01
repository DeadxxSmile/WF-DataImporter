import os
import requests
import re
import subprocess
import json


def remove_temp_files(remove_loc):
    # Remove files from temporary folder
    for filename in os.listdir(remove_loc):
        file_path = os.path.join(remove_loc, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def get_wf_key(key_url, key_download):
    response = requests.get(key_url)
    response.raise_for_status()
    with open(key_download, "wb") as f:
        f.write(response.content)


def expand_lzma(input_path, output_path):
    # Check if the input file exists
    if not os.path.exists(input_path):
        print("The input file does not exist.")
        exit()

    # Decompress the file using 7z
    try:
        seven_zip_path = os.path.join(os.environ["ProgramFiles"], "7-Zip", "7z.exe")
        subprocess.run(
            [seven_zip_path, "x", input_path, f"-o{output_path}", "-y"], check=True
        )
        print(f"File decompressed successfully and saved to {output_path}")
    except Exception as e:
        print(f"An error occurred during decompression: {e}")


def get_wf_data(download_path, current_key, data_link):
    # Set key file information
    key_file = os.path.join(current_key, "index_en.txt")

    with open(key_file, "r") as f:
        key_data = f.read().splitlines()

    for key_name in key_data:
        current_url = data_link + key_name
        current_file = key_name.split("!")
        current_path = os.path.join(download_path, current_file[0])
        try:
            response = requests.get(current_url)
            response.raise_for_status()
            with open(current_path, "wb") as f:
                f.write(response.content)
        except Exception as e:
            print(f"Failed to download {current_url}: {e}")


def repair_json(json_folder_path, json_cleaned_folder):
    # Get all JSON files in the specified folder
    json_files = [f for f in os.listdir(json_folder_path) if f.endswith(".json")]

    for json_file in json_files:
        # Get current JSON file path
        json_file_path = os.path.join(json_folder_path, json_file)

        # Set cleaned JSON file path
        file_name_parts = json_file.split(".")
        json_cleaned_path = os.path.join(
            json_cleaned_folder, f"{file_name_parts[0]}_Cleaned.{file_name_parts[1]}"
        )

        # Clean JSON file of any new lines before/after '\r' carriage return
        with open(json_file_path, "r", encoding="utf-8") as file:
            json_content = file.read()

            # Remove newlines and spaces before/after '\r' while keeping valid JSON formatting
            json_cleaned = re.sub(r"\s*\\r\s*", r"\\r", json_content)
            json_cleaned = re.sub(r"\s*\\n\s*", r"\\n", json_cleaned)

        # Load the cleaned JSON data
        json_data = json.loads(json_cleaned)

        # Apply the 'masteryReq' fix only if the file is 'ExportWeapons_en.json'
        if json_file == "ExportWeapons_en.json":
            for weapon in json_data.get("ExportWeapons", []):
                keys = list(weapon.keys())
                seen_mastery_req = False
                for key in keys:
                    if key == "masteryReq":
                        if seen_mastery_req:
                            del weapon[key]
                        else:
                            seen_mastery_req = True

        # Export the fully cleaned JSON data
        with open(json_cleaned_path, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4)


def main():
    # Set folder paths
    script_root = os.path.dirname(os.path.abspath(__file__))
    temp_folder = os.path.join(script_root, "temp")
    key_dir = os.path.join(script_root, "Keys")
    wf_data_dir = os.path.join(script_root, "JSON/Public")

    # Set URLs for Warframe data & key download filename
    key_url = "https://origin.warframe.com/PublicExport/index_en.txt.lzma"
    wf_data_url = "http://content.warframe.com/PublicExport/Manifest/"
    key_download = os.path.join(temp_folder, "index_en.txt.lzma")

    try:
        # Get the current key file and save to temp folder
        get_wf_key(key_url, key_download)

        # Expand the LZMA archive and save to keys folder
        expand_lzma(key_download, key_dir)

        # Download Warframe data files to temp folder
        get_wf_data(temp_folder, key_dir, wf_data_url)

        # Fix issues with Warframe JSON files and export to JSON folder
        repair_json(temp_folder, wf_data_dir)
    except Exception as e:
        # Output error message
        print(f"Main Code Try/Catch Block - An error occurred: {e}")
    finally:
        # Clean temporary files out of temp folder
        remove_temp_files(temp_folder)
        print("Done")


if __name__ == "__main__":
    main()
