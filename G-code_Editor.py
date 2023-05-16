import string 

new_code=""

with open("xyz-10mm-calibration-cube_0.4n_0.2mm_PLA_MK4_8m.gcode", 'r') as f:
    code=list(map(str,f.read().split("\n")))
    
    #print(code[len(code)-2])   
    
if code[i][0] == ";": #Cette ligne est un commentaire, on le recopie simplement 
    new_code += code
       
    

with open("new-xyz-10mm-calibration-cube_0.4n_0.2mm_PLA_MK4_8m.gcode", "w") as fichier:
    fichier.write(new_code)
