import math
import json
import re
def quanta(MBD):
    return MBD/16

def QIPSHud(baseIPS, modIPS, quantum):
    IPSDamage = round(baseIPS*((1+modIPS)/quantum),2)*quantum
    return IPSDamage

def QEDHUD(baseED, totalDMG, EDMOds, quantum):
    QED = round((baseED+totalDMG*EDMOds)/quantum,2)*quantum
    return QED

def QIPSGame(baseIPS, modIPS, quantum):
    IPSDamage = round(round((baseIPS*(1+modIPS)/quantum),None)*quantum,3)
    return IPSDamage

def QEDGame(baseED, totalDMG, EDMOds, quantum):
    QED = round(round((baseED+totalDMG*EDMOds)/quantum,None)*quantum, 3)
    return QED

def loadMods(json_path):
    with open(json_path) as file:
        data = json.load(file)
    
    mods= {}
    
    for mod in data["ExportUpgrades"]:
       
        modName = mod["name"]
            
        mods[modName] = {

            "fusionLimit": mod.get("fusionLimit", 0),
            "type": mod.get("type","Unknown"),
            "levels": {
                level: stats for level, stats in enumerate(mod.get("levelStats", []))
            }
        }
        
    
    return mods

def loadWeps(json_path):
   
    with open(json_path) as file:
        data = json.load(file)
    
    
    weapons = {}
    
    damage_types_IPS = ["Impact", "Puncture", "Slash"]
    damage_types_ED = ["Heat", "Cold", "Electric", "Toxin", "Blast", "Radiation", "Gas", 
        "Magnetic", "Viral", "Corrosive", "Void"]
    
    
    for weapon in data["ExportWeapons"]:
        weaponName = weapon["name"]
        
        damageIPS = {damage_types_IPS: weapon["damagePerShot"][i] for i, damage_types_IPS in enumerate(damage_types_IPS)}
        damageED = {damage_types_ED: weapon["damagePerShot"][i+3] for i, damage_types_ED in enumerate(damage_types_ED)}
        
        weapons[weaponName] = {
            "productCategory": weapon.get("productCategory", ""),
            "totalDamage": weapon.get("totalDamage", 0),
            "criticalChance": weapon.get("criticalChance", 0),
            "criticalMultiplier": weapon.get("criticalMultiplier", 1),
            "procChance": weapon.get("procChance", 0),
            "fireRate": weapon.get("fireRate", 0),
            "magazineSize": weapon.get("magazineSize", 0),
            "reloadTime": weapon.get("reloadTime", 0),
            "multishot": weapon.get("multishot", 1),
            "damageIPS": damageIPS,
            "damageED": damageED,
            "quanta": quanta(weapon.get("totalDamage", 0))
            
        }
        

   
    return weapons

# def extractModInfo(level_stats):
#     elementalInfo = []
#     other = []
    
#     pattern = r"\+(\d+%) <DT_([A-Z]+)>([A-Za-z]+)"
    
#     for level in level_stats:
#         for stat in level["stats"]:
#             match = re.search(pattern, stat)
#             if match:
#                 percentage = match.group(1)
#                 elementCode = match.group(2)
#                 elementName = match.group(3)
#                 elementalInfo.append({"percentage":percentage, "element": elementName, "elementCode":elementCode})
#             else:
#                 other.append(stat)
#     return elementalInfo, other
# def extractModInfo(level_stats):
#     elementalInfo = []
#     other = []
    
#     pattern = r"\+(\d+%) <DT_([A-Z]+)>([A-Za-z]+)"
    
#     for level in level_stats:
#         if isinstance(level, dict) and "stats" in level:  # Check that level is a dictionary and contains "stats"
#             for stat in level["stats"]:
#                 match = re.search(pattern, stat)
#                 if match:
#                     percentage = match.group(1)
#                     elementCode = match.group(2)
#                     elementName = match.group(3)
#                     elementalInfo.append({"percentage": percentage, "element": elementName, "elementCode": elementCode})
#                 else:
#                     other.append(stat)
#         else:
#             # Handle the case where level is not in the expected format
#             print(f"Unexpected format in level_stats: {level}")
    
#     return elementalInfo, other

# def extractModInfo(level_stats):
#     elementalInfo = []
#     other = []
    
#     pattern = r"\+(\d+%) <DT_([A-Z]+)>([A-Za-z]+)"
    
#     for stat in level_stats:
#         if isinstance(stat, str):  # Handle the case where 'stats' is a list of strings
#             match = re.search(pattern, stat)
#             if match:
#                 percentage = match.group(1)
#                 elementCode = match.group(2)
#                 elementName = match.group(3)
#                 elementalInfo.append({"percentage": percentage, "element": elementName, "elementCode": elementCode})
#             else:
#                 other.append(stat)
#         else:
#             # Handle unexpected formats
#             print(f"Unexpected format in level_stats: {stat}")
    
#     return elementalInfo, other
def extractModInfo(level_stats):
    elementalInfo = []
    other = []
    
    pattern = r"\+(\d+%) <DT_([A-Z]+)>([A-Za-z]+)"
    
    for stat in level_stats:
        if isinstance(stat, str):  # Handle the case where 'stats' is a list of strings
            match = re.search(pattern, stat)
            if match:
                percentage = match.group(1)
                elementCode = match.group(2)
                elementName = match.group(3)
                elementalInfo.append({"percentage": percentage, "element": elementName, "elementCode": elementCode})
            else:
                other.append(stat)
        else:
            # Handle unexpected formats
            print(f"Unexpected format in level_stats: {stat}")
    
    return elementalInfo, other
def getModInfo(modlist, mods):
    mod_info = []
    elementalMods = []

    for mod in modlist:
        if mod in mods:
            max_rank = mods[mod]["fusionLimit"]
            mod_data = mods[mod]["levels"].get(max_rank, {})
            level_stats = mod_data.get("stats", [])
            
            if isinstance(level_stats, list):
                elementalInfo, otherStats = extractModInfo(level_stats)
                mod_info.append({
                    "name": mod, 
                    "max_rank": max_rank, 
                    "data": mod_data,
                    "elementalInfo": elementalInfo,
                    "otherStats": otherStats
                })
                if elementalInfo:
                    elementalMods.append({"name": mod, "elementalInfo": elementalInfo})
            else:
                print(f"Unexpected format in mod_data: {mod_data}")
    
    return mod_info, elementalMods

# def getModInfo(modlist, mods):
#     mod_info = []
#     elementalMods = []

#     for mod in modlist:
#         if mod in mods:
#             max_rank = mods[mod]["fusionLimit"]
#             mod_data = mods[mod]["levels"].get(max_rank, {})
#             level_stats = mod_data.get("stats", [])
            
#             if isinstance(level_stats, list):
#                 elementalInfo, otherStats = extractModInfo(level_stats)
#                 mod_info.append({
#                     "name": mod, 
#                     "max_rank": max_rank, 
#                     "data": mod_data,
#                     "elementalInfo": elementalInfo,
#                     "otherStats": otherStats
#                 })
#                 if elementalInfo:
#                     elementalMods.append({"name": mod, "elementalInfo": elementalInfo})
#             else:
#                 print(f"Unexpected format in mod_data: {mod_data}")
    
#     return mod_info, elementalMods



# def getModInfo(modlist, mods):
#     mod_info = []
#     elementalMods = []

#     for mod in modlist:
#         if mod in mods:
#             max_rank = mods[mod]["fusionLimit"]
#             mod_data = mods[mod]["levels"].get(max_rank, {})
#             elementalInfo, otherStats = extractModInfo(mod_data.get("stats",[]))
#             mod_info.append({"name": mod, "max_rank": max_rank, "data": mod_data,"elementalInfo": elementalInfo,"otherStats": otherStats})
#             if elementalInfo:
#                 elementalMods.append({"name":mod, "elementalInfo": elementalInfo})
#     return mod_info, elementalMods

def main():
    weapons = loadWeps('../JSON/2024-08-25/ExportWeapons_en_Cleaned.json')
    mods = loadMods('../JSON/2024-08-25/ExportUpgrades_en_Cleaned.json')
    
    name = input("Weapon Name: ")
    
    modlist = []
    while True:
        modIn = input('Enter mod name (done to finish): ')
        if modIn.lower() == 'done':
            break
        modlist.append(modIn)
    
    modInfo, elementalMods = getModInfo(modlist, mods)
    print("Mod Info:", modInfo)
    print("Elemental Mods", elementalMods)
    return   

if __name__ == "__main__":
    main()