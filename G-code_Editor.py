import string 

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