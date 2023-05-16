import string 

new_code=""  
#print(code[len(code)-2])   


def Main() :
    #Interraction avec l'utilisateur 
    
         
    #Extraction du G-code inital et séparation des lignes
    with open("xyz-10mm-calibration-cube_0.4n_0.2mm_PLA_MK4_8m.gcode", 'r') as f:
        code=list(map(str,f.read().split("\n")))
    
    if code[i][0] == ";": #Cette ligne est un commentaire, on le recopie simplement 
        new_code += code 
       
    #Ecriture du G-code mis à jour dans un nouveau fichier
    with open("new-xyz-10mm-calibration-cube_0.4n_0.2mm_PLA_MK4_8m.gcode", "w") as fichier:
        fichier.write(new_code)