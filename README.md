# Projet-Editeur-G-code

# Comprehension g-code

M204 [P<accel>] : règle l'accélération d'un mvt

G0, G1 [E<pos>] [X<pos>] [Y<pos>] [Z<pos>] [F<rate>] : mouvement linaires avec E la quantité de filament, X Y et Z la nouvelle coordonnée, F est la vitesse de déplacement de la tête

M104 [S<temp>] : set target temp sans attendre

M109 [S<temp>] : set tercet temp et attendre de l'atteindre
