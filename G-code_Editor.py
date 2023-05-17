import string 

TEMP_FUSION = 225
Code_modifie=""  
#print(code[len(code)-2])   

def Calcul_nombre_couche(code) : 
    #calcul nb couche
    Nb_couche = 50
    return Nb_couche

def Modification_Temperature (Couche):
    print("")
    

def Main() :
    #********Extraction du G-code inital et séparation des lignes********
    with open("xyz-10mm-calibration-cube_0.4n_0.2mm_PLA_MK4_8m.gcode", 'r') as f:
        code=list(map(str,f.read().split("\n")))
    
    NB_COUCHE = Calcul_nombre_couche(code) #Calcul du nombre de couche 
    
    #********Interraction avec l'utilisateur********
    NombrePhase = int(input("Entrez le nombre de phase que vous désirez pour la variation de la température : "))
    
    for i in range (0,NombrePhase):
        Temperature_Min = input(f"Entrez la temperature minimum pour la phase {i}: ")
        if Temperature_Min < TEMP_FUSION :
            print(f"Attention, la température se trouve en dessous du point de fusion du thermoplastique ({TEMP_FUSION})")
            Temperature_Min = input(f"Entrez une nouvelle temperature minimum pour la phase {i}: ")
        Temperature_Max = input(f"Entrez la temperature maximum pour la phase {i}: ")
        Nombre_Couche = input(f"Entrez le nombre de couche comprises dans la phase {i}: " )
        Phase.append((Temperature_Min,Temperature_Max,Nombre_Couche))
    
         
    
    if code[i][0] == ";": #Cette ligne est un commentaire, on le recopie simplement 
        Code_modifie += code 
       
    #Ecriture du G-code mis à jour dans un nouveau fichier
    with open("new-xyz-10mm-calibration-cube_0.4n_0.2mm_PLA_MK4_8m.gcode", "w") as fichier:
        fichier.write(new_code)