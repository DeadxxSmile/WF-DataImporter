% Parameters
x = 57;  
base = 8;  
baseArmor = 500;  
armorCap = 2700;  
originalDamage = 50;  


LevelDiff = x - base;


if LevelDiff < 70
    S1 = 0;
elseif LevelDiff > 80
    S1 = 1;
else
    S1 = (LevelDiff - 70) / 10;  
end


f1 = 1 + 0.005 * (LevelDiff)^1.75;
f2 = 1 + 0.4 * (LevelDiff)^0.75;


armorMultiplier = (f1 * (1 - S1)) + (f2 * S1);

 
finalArmor = baseArmor * armorMultiplier;


finalArmor = min(finalArmor, armorCap);


damageReduction = 0.9 * sqrt(finalArmor / 2700);


finalDamage = originalDamage * (1 - damageReduction);


disp(['Level Difference: ', num2str(LevelDiff)]);
disp(['S1: ', num2str(S1)]);
disp(['f1: ', num2str(f1)]);
disp(['f2: ', num2str(f2)]);
disp(['Armor Multiplier: ', num2str(armorMultiplier)]);
disp(['Final Armor Value: ', num2str(finalArmor)]);
disp(['Damage Reduction: ', num2str(damageReduction)]);
disp(['Final Damage: ', num2str(finalDamage)]);
