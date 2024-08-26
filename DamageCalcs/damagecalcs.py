import math
import json
def quanta(MBD):
    return MBD/16

def QIPS(baseIPS, modIPS, quantum):
    IPSDamage = round((baseIPS*((1+modIPS)/quantum)*quantum),0.1)
    return IPSDamage

def QED(baseED, MBD, EDMOds, quantum):
    QED = round((baseED+MBD*EDMOds)/quantum,0.1)*quantum
    
def main():
    with open('C:/Users/alexc/Downloads/Warframe-JSON-04-08-24/ExportWeapons_en_Cleaned.json') as file:
        data = json.load(file)
    name = input("Weapon Name: ")
    weapon = None
    
    for i in data["ExportWeapons"]:
        if name == i["name"]:
            weapon = i
            break
    if weapon is None:
       print(f"Weapon {name} not found")   
        

    damage_types_IPS = ["Impact", "Puncture", "Slash"]
    damage_types_ED = ["Heat", "Cold", "Electric", "Toxin", "Blast", "Radiation", "Gas", 
        "Magnetic", "Viral", "Corrosive", "Void"]
    stats_types = ["totalDamage", "criticalChance", "criticalMultiplier", "procChance", "fireRate", "productCategory", 
            "accuracy", "omegaAttenuation", "noise", "trigger", "magazineSize", "reloadTime", "multishot"]
    damageIPS = {damage_types_IPS: weapon["damagePerShot"][i] for i, damage_types_IPS in enumerate(damage_types_IPS)}
    damageED = {damage_types_ED: weapon["damagePerShot"][i+3] for i, damage_types_ED in enumerate(damage_types_ED)}
    stats = {stat: weapon.get(stat, None) for stat in stats_types}
    print(damageIPS)
    print(damageED)
    print(stats)
    
    
    

if __name__ == "__main__":
    main()