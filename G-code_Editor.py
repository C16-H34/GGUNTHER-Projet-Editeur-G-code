import string
import numpy as np 
import matplotlib.pyplot as plt

TEMP_FUSION = 225 #En dessous de cette température, impossible d'imprimer car le thermoplastique n'est pas suffisamment visqueux

'''FONCTIONS'''

'''ECRITURE crée le nouveau code de la couche à partir du code source(code_couche), de ratio_speed, ratio_extrud et temp_tete
'''

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
        
        
        
        
        
        

##FONCTIONS

#fonction d'ecriture qui crée le nouveau code de la couche à partir du code source(code_couche), de ratio_speed, ratio_extrud et temp_tete
def ecriture(temp_tete, ratio_speed, ratio_extrud, code_couche):
    #initialisation de newcouche, la liste qui sera retournée par la fonction
    newcouche = []
    #on chauffe la tete a la temperature desiree au debut de chaque couche
    newcouche.append('M104 S' + str(temp_tete))
    newcouche.append('M109 R' + str(temp_tete))

    #parcours des lignes de la couche 
    for ligne in code_couche:
        #initialisation de newligne, string qui contiendra la nouvelle ligne modifiée
        newligne = ''

        #si la ligne est vide alors on ne la modifie pas : nécessaire car tout test d'index renvoie une erreur sur une string vide
        if ligne == '':
            newligne = ligne
            newcouche.append(newligne)
            continue
        #sinon, si la ligne est une commentaire, on ne la modifie pas
        elif ligne[0] == ';':
            newligne = ligne
            newcouche.append(newligne)
            continue
        #sinon, on cherche si il y a un commentaire dans la ligne et on note son index, cela nous sera util par la suite
        else:
            icom = ligne.find(';')
        
        #on parcourt les mots de la ligne
        for mot in ligne.split():
            #initialisation de newmot, c'est le mot modifié a ecrire sur la nouvelle ligne
            newmot = ''

            #Si le mot est le début d'un commmentaire, on ecrit la partie de ligne déjà modifiée suivie du commantaire, on sort de la boucle car la ligne entiere est désormais traitée
            if ';' in mot:
                newligne += ligne[icom:]
                break
            #sinon, si le mot gere l'extrudation, effectuer sa modification avec ratio_extrud
            elif (mot[0] == 'E' and len(mot)>1):
                extrud = str(float(mot[1:]) + (ratio_extrud*float(mot[1:])))
                newmot = 'E' + extrud[1:6]
            #sinon, si le mot gere la vitesse d'impression, effectuer la modification avec ratio_speed
            elif mot[0] == 'F':
                speed = str(int((ratio_speed*int(mot[1:]))))
                newmot = 'F' + speed
            #sinon, on ne doit pas modifier le mot
            else:
                newmot = mot
            
            #on ajoute le mot modifié a la nouvelle ligne
            newligne += (newmot + ' ')

        #on ajoute la ligne modifiée à la nouvelle couche 
        newcouche.append(newligne)

    #on retourne la couche modifiée
    return newcouche


    
def modifier_temp():
    return 140


def modifier_vitesse():
    return 0.9

def modifier_extrud():
    return 0.1


## MAIN CODE 
#Interraction avec l'utilisateur 
    
         
#Extraction du G-code inital et séparation en couche : ATTENTION la séparation n'est pas parfaite et des commentaires sont comptés comme couches
with open("xyz-10mm-calibration-cube_0.4n_0.2mm_PLA_MK4_8m.gcode", 'r') as f:
     code=list(map(str,f.read().split("\n\n")))

#initialisation de newcode : la liste qui contiendra le code modifié séparé par couche
newcode = []

#on parcourt les couches
for couche in code:
    #séparation de la couche par ligne de code
    code_couche = couche.split("\n")

    #détermination de temp_tete, ratio_speed et ratio_extrud avec les fonctions
    #temp_tete est la temperature de la tete en degres celsius
    #ratio_speed est le coefficient multiplicateur de la vitesse d'impressin pour la couche
    #ratio_extrud est le le pourcentage de sur-extrudation ou sous-extrudation, il est ecrit en décimal, positif pour la sur-extrudation et négatif pour la sous-extrudation
    temp_tete = modifier_temp()
    ratio_speed = modifier_vitesse()
    ratio_extrud = modifier_extrud()

    #ecriture du nouveau code de la couche dans la liste newcouche
    newcouche = ecriture(temp_tete, ratio_speed, ratio_extrud, code_couche)
    #creation d'un string de la nouvelle couche 
    strnewcouche = '\n'.join(newcouche)
    #ecrittre du code modifié dans une liste newcode
    newcode.append(strnewcouche)
    newcode.append('\n')

#strnewcode est le string du nouveau code
strnewcode = '\n'.join(newcode)

#Ecriture du G-code mis à jour dans un nouveau fichier
with open("newgcode_cube.gcode", "w") as fichier:
    fichier.write(strnewcode)
    
Main()