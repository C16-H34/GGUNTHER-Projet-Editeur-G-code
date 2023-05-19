import string
import numpy as np 
import matplotlib.pyplot as plt

TEMP_FUSION = 225 #En dessous de cette température, impossible d'imprimer car le thermoplastique n'est pas suffisamment visqueux

'''CALCUL_NOMBRE_COUCHE parcours le fichier et renvoi le nombre de couche'''
def Calcul_nombre_couche(code) : 
    #calcul nb couche
    Nb_couche = 50
    return Nb_couche

'''CALCUL_TEMPERATURE retourne une liste contenant une valeur de température par couche. 
La variation est linéaire par phase. Les phases sont choisies par l'utiisateur'''
def Calcul_Temperature (Nombre_couche):
    
    #Choix du nombre de phase par l'utilisateur
    NombrePhase = int(input("Entrez le nombre de phase que vous désirez pour la variation de la température : "))
    while NombrePhase > Nombre_couche : #Gestion erreur si plus de phase que de couche
        print(f'Attention, nombre de phase supérieur au nombre de couches ({Nombre_couche}), recommencez')
        NombrePhase = int(input("Entrez une nouvelle valeur: "))
        
    #Choix des caractéristiques de chaques phases
    for i in range (0,NombrePhase+1):
        
        if i == 0 : #Première Phase (On demande seulement la température initiale)
            Temperature = int(input("Entrez la temperature désirée pour la première couche : "))
            while Temperature < TEMP_FUSION : #Gestion d'erreur si la température < point de fusion du thermoplastique
                print(f"Attention, la température se trouve en dessous du point de fusion du thermoplastique ({TEMP_FUSION})")
                Temperature = int(input(f"Entrez une nouvelle valeur: "))
            Tab_Temperature = np.array([Temperature]) 
               
        elif i == NombrePhase : #Dernière Phase (On demande seulement la température finale)
            Temperature = int(input("Entrez la temperature désirée pour la dernière couche : "))
            while Temperature < TEMP_FUSION : #Gestion d'erreur si la température < point de fusion du thermoplastique
                print(f"Attention, la température se trouve en dessous du point de fusion du thermoplastique ({TEMP_FUSION})")
                Temperature = int(input(f"Entrez une nouvelle valeur: "))       
            Temperature= np.linspace(Tab_Temperature[-1],Temperature,Nombre_couche-(len(Tab_Temperature)-1))
            Tab_Temperature =np.delete(Tab_Temperature,-1) #On supprime la dernière valeur pour éviter la redondance
            Tab_Temperature=np.append(Tab_Temperature,[Temperature])
            
        else : #Phase intermédiaire (On demande la température finale ET la couche finale de la phase)
            Temperature = int(input(f"Entrez la temperature atteinte à la fin de la phase {i}: "))
            while Temperature < TEMP_FUSION : #Gestion d'erreur si la température est inférieure au point de fusion du thermoplastique
                print(f"Attention, la température se trouve en dessous du point de fusion du thermoplastique ({TEMP_FUSION}), recommencez")
                Temperature = int(input(f"Entrez une nouvelle temperature: "))    
            Couche_Finale = int(input(f"Entrez le numéro de la dernière couche inclue dans la phase {i}: " ))
            while Couche_Finale > Nombre_couche :
                print(f"Attention, vous avez dépassé le nombre de couche ({Nombre_couche}), recommencez")
                Couche_Finale = int(input(f"Entrez une nouvelle temperature: "))
                    
            Temperature= np.linspace(Tab_Temperature[-1],Temperature,Couche_Finale-(len(Tab_Temperature)-1))
            Tab_Temperature =np.delete(Tab_Temperature,-1) #On supprime la dernière valeur pour éviter la redondance
            Tab_Temperature=np.append(Tab_Temperature,[Temperature])
    
    #Affichage à l'utilisateur du profil de variation de température souhaité
    plt.plot(np.linspace(1,Nombre_couche,Nombre_couche),Tab_Temperature,color='r')
    plt.title("Evolution de la température selon les couches d'impression",loc="center")
    plt.xlabel('Couches d\'impression')
    plt.ylabel('Température de la tête d\'impression')
    plt.show()
    
    return Tab_Temperature    
    
'''MAIN est la fonction principale du fichier'''       
def Main() :
    #********Extraction du G-code inital et séparation des lignes********
    with open("xyz-10mm-calibration-cube_0.4n_0.2mm_PLA_MK4_8m.gcode", 'r') as f:
        gcode=list(map(str,f.read().split("\n")))
    #********Calcul des paramètres***********
    NB_COUCHE = Calcul_nombre_couche(gcode) 
    Temperature = Calcul_Temperature(NB_COUCHE)
    
''' #*******Traitement du fichier*********
    if code[i][0] == ";": #Cette ligne est un commentaire, on le recopie simplement 
        Code_modifie += code 
       
    #*******Ecriture du G-code mis à jour dans un nouveau fichier*********
    with open("new-xyz-10mm-calibration-cube_0.4n_0.2mm_PLA_MK4_8m.gcode", "w") as fichier:
        fichier.write(Code_modifie)'''
        
        
        
Main()