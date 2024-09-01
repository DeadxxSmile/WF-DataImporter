import json
import os

def clean_mastery_req(export_dir,import_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_dir = os.path.join(script_dir, export_dir)
    json_file_path = os.path.join(script_dir, export_dir, import_path)
    json_export_path = os.path.join(json_dir, "ExportWeapons_en_Fixed.json")
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    for weapon in json_data.get("ExportWeapons", []):
        keys = list(weapon.keys())
        seen_mastery_req = False
        for key in keys:
            if key == "masteryReq":
                if seen_mastery_req:
                    del weapon[key]
                else:
                    seen_mastery_req = True
                    
    with open(json_export_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4)
        
    return print(f"Cleaned JSON file saved to: {json_export_path}")
        

def main():
    jsonDIR = 'JSON/Public'
    inputJSON = 'ExportWeapons_en_Cleaned.json'
    
    clean_mastery_req(jsonDIR, inputJSON)

if __name__ == "__main__":
    main()