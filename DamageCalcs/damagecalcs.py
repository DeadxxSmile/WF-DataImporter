import math
import json
import re

def quanta(MBD):
    return MBD / 16

def QIPSHud(baseIPS, modIPS, quantum):
    IPSDamage = round(baseIPS * ((1 + modIPS) / quantum), 2) * quantum
    return IPSDamage

def QEDHUD(baseED, totalDMG, EDMOds, quantum):
    QED = round((baseED + totalDMG * EDMOds) / quantum, 2) * quantum
    return QED

def QIPSGame(baseIPS, modIPS, quantum):
    IPSDamage = round(round((baseIPS * (1 + modIPS) / quantum), None) * quantum, 3)
    return IPSDamage

def QEDGame(baseED, totalDMG, EDMOds, quantum):
    if baseED == 0:
        return round(round(totalDMG * EDMOds / quantum) * quantum,3)#check
        
    else:
        return round(round((baseED + totalDMG * EDMOds) / quantum) * quantum, 3)#check

def enemyGameIPS(baseIPS, modIPS, quantum, armour, enemyVal): 
   
    IPS = round(round((baseIPS * (1 + modIPS)) / quantum) * quantum, 3) * ((1 - armour) * enemyVal)

    return IPS

def enemyGameQED(baseED, totalDMG, EDMods, quantum, armour, enemyVal):
    if baseED == 0:
        QED = round(round((totalDMG*EDMods)/quantum,0)*quantum,3)*((1-armour)*enemyVal)
    else: 
        QED = round(round((baseED+totalDMG*EDMods)/quantum,0)*quantum,3)*((1-armour)*enemyVal)
    return QED

def loadEnemy(json_path):
    with open(json_path) as file:
        data = json.load(file)
        
    enemies = {}
    
    for enemy in data["ExportEnemyValues"]:
        enemyName = enemy.get("name", "Unnamed Enemy")
        
        if enemyName not in enemies:
            enemies[enemyName] = []
            
        enemies[enemyName].append({
            "Impact": enemy.get("Impact", 1),
            "Puncture": enemy.get("Puncture", 1),
            "Slash": enemy.get("Slash", 1),
            "Heat": enemy.get("Heat", 1),
            "Cold": enemy.get("Cold", 1),
            "Electricity": enemy.get("Electricity", 1),
            "Toxin": enemy.get("Toxin", 1),
            "Blast": enemy.get("Blast", 1),
            "Magnetic": enemy.get("Magnetic", 1),
            "Viral": enemy.get("Viral", 1),
            "Corrosive": enemy.get("Corrosive", 1),
            "Void": enemy.get("Void", 1),
            "Radiation": enemy.get("Radiation", 1),
            "Gas": enemy.get("Gas", 1),
            "True": enemy.get("True", 1)
        })
    return enemies


def loadMods(json_path):
    with open(json_path) as file:
        data = json.load(file)
    
    mods = {}
    
    for mod in data["ExportUpgrades"]:
        modName = mod.get("name", "Unnamed Mod")
        uniqueName = mod.get("uniqueName", "Unknown Unique Name")
        
        if modName not in mods:
            mods[modName] = []

        mods[modName].append({  
            "uniqueName": uniqueName,
            "fusionLimit": mod.get("fusionLimit", 0),
            "type": mod.get("type", "Unknown"),
            "levels": {
                level: stats for level, stats in enumerate(mod.get("levelStats", []))
            }
        })
    
    return mods

def loadWeps(json_path):
    with open(json_path) as file:
        data = json.load(file)
    
    weapons = {}
    
    damage_types_IPS = ["Impact", "Puncture", "Slash"]
    damage_types_ED = ["Heat", "Cold", "Electricity", "Toxin", "Blast", "Radiation", "Gas", 
        "Magnetic", "Viral", "Corrosive", "Void"]
    
    for weapon in data["ExportWeapons"]:
        weaponName = weapon["name"]
        
        damageIPS = {damage_type: weapon["damagePerShot"][i] for i, damage_type in enumerate(damage_types_IPS)}
        damageED = {damage_type: weapon["damagePerShot"][i + len(damage_types_IPS)] for i, damage_type in enumerate(damage_types_ED)}
        
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

def extractModInfo(level_stats):
    elementalInfo = []
    other = []
    
    pattern = r"\+(\d+%) <DT_([A-Z]+)>([A-Za-z]+)"
    
    for stat in level_stats:
        if isinstance(stat, str): 
            match = re.search(pattern, stat)
            if match:
                percentage = match.group(1)
                elementName = match.group(3)
                elementalInfo.append({"percentage": percentage, "element": elementName})
            else:
                other.append(stat)
        else:
            print(f"Unexpected format in level_stats: {stat}")
    
    return elementalInfo, other

def getModInfo(modlist, mods):
    mod_info = []

    for mod in modlist:
        possible_mods = mods.get(mod, [])
        
        if len(possible_mods) > 1:
            print(f"Multiple mods found for '{mod}'. Please choose one based on max rank percentage:")
            for idx, possible_mod in enumerate(possible_mods):
                max_rank = possible_mod["fusionLimit"]
                max_stats = possible_mod["levels"].get(max_rank, {}).get("stats", [])
                max_percentage = None
                for stat in max_stats:
                    match = re.search(r"\+(\d+%)", stat)
                    if match:
                        max_percentage = match.group(1)
                        break
                print(f"{idx + 1}: {possible_mod['uniqueName']} with max {max_percentage}")
            choice = int(input("Enter the number of the mod you want to use: ")) - 1
            chosen_mod = possible_mods[choice]
        elif len(possible_mods) == 1:
            chosen_mod = possible_mods[0]
        else:
            print(f"No mod found with the name '{mod}'.")
            continue
        
        max_rank = chosen_mod["fusionLimit"]
        mod_data = chosen_mod["levels"].get(max_rank, {})
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
            
        else:
            print(f"Unexpected format in mod_data: {mod_data}")
    
    return mod_info

def getEnemyInfo(enemy, name):
    enemy_data = enemy.get(name, [{}])[0]
    return enemy_data
    

def combine_elemental_mods(modInfo):
    combinedElements = {
        "Corrosive": ("Electricity", "Toxin"),
        "Blast": ("Heat", "Cold"),
        "Radiation": ("Heat", "Electricity"),
        "Gas": ("Heat", "Toxin"),
        "Magnetic": ("Cold", "Electricity"),
        "Viral": ("Cold", "Toxin")
    }
    
    activeElements = {}
    
    for mod in modInfo:
        for elem in mod["elementalInfo"]:
            element = elem["element"]
            percentage = float(elem["percentage"].strip("%")) / 100
            if element in activeElements:
                activeElements[element] += percentage
            else:
                activeElements[element] = percentage
    
    combinedMods = {}
    
    for combo, elements in combinedElements.items():
        if all(elem in activeElements for elem in elements):
            combinedMods[combo] = activeElements[elements[0]] + activeElements[elements[1]]
          
            del activeElements[elements[0]]
            del activeElements[elements[1]]
    
   
    combinedMods.update(activeElements)
    
    return combinedMods

def weaponDamageQuantised(weapon, mod_info, enemyInfo, armour):
    damageCalcGame = []
    damageCalcHUD = []
    damageCalcEnemy = []
    base_damage = weapon["totalDamage"]
    quantum = weapon["quanta"]
    
   
    for damageType, base_value in weapon["damageIPS"].items():
        modVal = 0
        for mod in mod_info:
            for ips in mod["elementalInfo"]:
                if damageType == ips["element"]:
                    modVal += float(ips["percentage"].strip("%")) / 100  
        quantDamageGame = QIPSGame(base_value, modVal, quantum)
        quantDamageHUD = QIPSHud(base_value, modVal, quantum)
        quantDamageEnemy = enemyGameIPS(base_value,modVal, quantum, armour, enemyInfo.get(damageType, 1))
        damageCalcGame.append({"type": damageType, "value": quantDamageGame})
        damageCalcHUD.append({"type": damageType, "value": quantDamageHUD})
        damageCalcEnemy.append({"type": damageType, "value": quantDamageEnemy})
  
    combined_mods = combine_elemental_mods(mod_info)
    
   
    for damageType, base_value in weapon["damageED"].items():
        modVal = combined_mods.get(damageType, 0)
        
        quantDamageGame = QEDGame(base_value, base_damage, modVal, quantum)
        quantDamageHUD = QEDHUD(base_value, base_damage, modVal, quantum)
        quantDamageEnemy = enemyGameQED(base_value, base_damage, modVal, quantum, armour, enemyInfo.get(damageType,1))
        damageCalcGame.append({"type": damageType, "value": quantDamageGame})
        damageCalcHUD.append({"type": damageType, "value": quantDamageHUD})
        damageCalcEnemy.append({"type": damageType, "value": quantDamageEnemy})
    
    
    return damageCalcGame, damageCalcHUD, damageCalcEnemy

def damageModifiers(modInfo):
    modVal = 0
    pattern = r"\+(\d+%) Damage"  
    for mod in modInfo:
        for stat in mod["otherStats"]:
            match = re.match(pattern, stat)
            if match:
                percentage = match.group(1)
                modVal += float(percentage.strip("%")) / 100

    
    return modVal

def armourModifer(num)                :
    armour = 0.9*math.sqrt(num/2700)
    return armour
def banes(modInfo, damageCalced, modifiers):
    pattern = r"x(\d+\.\d+) Damage to (.+)"
    for mod in modInfo:
        for stat in mod["otherStats"]:  
            match = re.match(pattern, stat)
            if match:
                multiplier = float(match.group(1))
                bane_damage = round((damageCalced + damageCalced * modifiers) * multiplier, None)
                print(f"Bane applied: {stat}, Multiplier: {multiplier}, Damage: {bane_damage}")
                return bane_damage  
    return None  

def dmgTotals(dmgGame, dmgHud, dmgEnemy):
    gameDMG = 0
    hudDMG = 0
    enemyDMG = 0
    for dmg in dmgGame:
        gameDMG += dmg['value']
    for dmg in dmgHud:
        hudDMG += dmg['value']
    for dmg in dmgEnemy:
        enemyDMG += dmg['value']
    return gameDMG, hudDMG, enemyDMG
    
def main():
    weapons = loadWeps('../JSON/2024-08-25/ExportWeapons_en_Cleaned.json')
    mods = loadMods('../JSON/2024-08-25/ExportUpgrades_en_Cleaned.json')
    enemies = loadEnemy('../JSON/Custom/ExportEnemyValues.json')
    ###############
    #Set Hard Codes for testing
    ###############
    
    # name = input("Weapon Name: ")
    name = "Baza Prime"
    # modlist = []
    modlist = ["Cryo Rounds", "Stormbringer", "Serration", "Piercing Caliber", "Bane of Grineer"]
    # while True:
    #     modIn = input('Enter mod name (done to finish): ')
    #     if modIn.lower() == 'done':
    #         break
    #     modlist.append(modIn)
        
    # nameEn = input("Enemy type Name: ")
    nameEn = "Grineer"
    # armourVal = float(input("Armour Value: "))
    armourVal = 389
    
    enemyInfo = getEnemyInfo(enemies, nameEn)
    modInfo = getModInfo(modlist, mods) 
    armour = armourModifer(armourVal)
    if name in weapons:
        weapon_data = weapons[name]
        damageCalcGame, damageCalcHUD, damageCalcEnemy = weaponDamageQuantised(weapon_data, modInfo, enemyInfo, armour)
        damageMods = damageModifiers(modInfo)
        game, hud, enemy = dmgTotals(damageCalcGame, damageCalcHUD, damageCalcEnemy)
        finalDMGGame = round(game+game*damageMods, 0)
        finalDMGHUD = round(hud+hud*damageMods,1)
        finalDMGEnemy = round(enemy+enemy*damageMods,0)
        bane1 = banes(modInfo,game,damageMods)
        bane2 = banes(modInfo,enemy,damageMods)
        print("Final Game Damage is: ", finalDMGGame)
        print("Final Enemy Damage is: ", finalDMGEnemy)
        print("Applied bane damage (true): ",bane1)
        print("Applied bane damage (armour): ", bane2)
        print("Final HUD Damage is: ", finalDMGHUD)
    else:
        print(f"Weapon {name} not found.")
    
if __name__ == "__main__":
    main()
