# coding: utf_8

Codé par : Octave FORTUN, Milo MONTAGNE, Pierrick LEFEVRE

Pseudo-code du Projet NSI 3 "Choixpeau Magique", partie I

Le programme utilise l'algorithme des k plus proches voisins pour attribuer 
une maison à un personnage en fonction de 4 caractéristiques 
(le courage, l'ambition, l'intelligence, la tendance au bien)
à l'aide d'une base de données de personnages d'Harry Potter

Licence : CC-BY-NC-SA

github : https://github.com/Fismoto/Choixpeau_Magique

DEBUT
	DEFINIR FONCTION distance(base_de_donnees_des_personnages, nouveau_personnage)

    		Cette fonction renvoie la table avec la clef 'Distance'
    		ajoutée à chaque dictionnaire.
    		La valeur de cette clef est la distance entre le new_character
    		et le personnage de la base de données symbolisé par le dictionnaire.
    		Cela nous servira pour l'algorithme des kPPV.

		Entrées :
			- base_de_donnees_des_personnages : table (tableau de dictionnaires) 
			où chaque dictionnaire  correspond à un personnage,
			avec comme clefs toutes les informations qu'on a sur ce personnage
			(dont au moins 'Maison', 'Courage', 'Ambition', 'Intelligence', 
			'Tendance au bien')

			- nouveau_personnage : dictionnaire qui correspond à un personnage
			avec comme clefs les caractéristiques qu'on a sur ce personnage
			('Courage', 'Ambition', 'Intelligence', 'Tendance au bien')
			Note : on ne connait pas la maison de ce personnage cible,
			c'est ce que l'on cherchera à déterminer avec l'algorithme des kPPV

		Sorties : 
			- base_de_donnees_avec_distance : table (tableau de dictionnaires)
			copie de base_de_donnees_des_personnages à laquelle on a ajouté à 
			chaque dictionnaire la clef 'Distance' qui correspond à la distance euclidienne 
			entre ce personnage et le personnage cible nouveau_personnage

		Préconditions :
			- base_de_donnees_des_personnages est un tableau composé uniquement de dictionnaires
			- nouveau_personnage  est un dictionnaire qui contient les clefs 'Courage', 
			'Ambition', 'Intelligence' et 'Good', ces clefs ont une valeur entre 1 et 9

		Variables :
			- base_de_donnees_avec_distance : tableau de dictionnaires
			- n : entier, longueur de base_de_donnees_des_personnages
			- distance : flottant, distance entre chaque personnage 
			et le personnage cible
		
		DEBUT
			base_de_donnees_avec_distance = COPIE de base_de_donnees_des_personnages
			n = longueur(base_de_donnees_des_personnages)

			POUR i ALLANT DE 0 A n - 1 
				distance = RACINE_CARRE((nouveau_personnage['Courage'] + base_de_donnees_des_personnages[i]['Courage'])**2
						     	+ (nouveau_personnage['Ambition'] + base_de_donnees_des_personnages[i]['Ambition'])**2
							+ (nouveau_personnage['Intelligence'] + base_de_donnees_des_personnages[i]['Intelligence'])**2
							+ (nouveau_personnage['Tendance au bien'] + base_de_donnees_des_personnages[i]['Tendance au bien'])**2)
				 base_de_donnees_avec_distance[i]['Distance'] = distance
			FIN POUR
		FIN

		RENVOYER base_de_donnees_avec_distance

	FIN DEFINIR FONCTION
		
