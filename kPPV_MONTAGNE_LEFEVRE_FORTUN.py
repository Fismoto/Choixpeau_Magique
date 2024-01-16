# coding: utf_8

'''
Codé par : Octave FORTUN, Milo MONTAGNE, Pierrick LEFEVRE

Projet NSI 3 "Choixpeau Magique", partie I

Le programme utilise l'algorithme des k plus proches voisins pour attribuer 
une maison à un personnage en fonction de 4 caractéristiques 
(le courage, l'ambition, l'intelligence, la tendance au bien)
à l'aide d'une base de données de personnages d'Harry Potter

Licence : CC-BY-NC-SA

github : https://github.com/Fismoto/Choixpeau_Magique
'''

# Importation des modules :
import csv
from math import sqrt


# Définition des fonctions :
def distance(characters_data_base, new_character):
    '''
    Cette fonction renvoie la table avec la clef 'Distance'
    ajoutée à chaque dictionnaire.
    La valeur de cette clef est la distance entre le new_character
    et le personnage de la base de données symbolisé par le dictionnaire.
    Cela nous servira pour l'algorithme des kPPV.
    
    Entrées :
        - characters_data_base : table (tableau de dictionnaires) 
        où chaque dictionnaire  correspond à un personnage,
        avec comme clefs toutes les informations qu'on a sur ce personnage
        (dont au moins 'House', 'Courage', 'Ambition', 'Intelligence', 'Good')

        - new_character : dictionnaire qui correspond à un personnage
        avec comme clefs les caractéristiques qu'on a sur ce personnage
        (dont au moins 'Courage', 'Ambition', 'Intelligence' et 'Good')
        Note : on ne connait pas la maison de ce personnage cible,
        c'est ce que l'on cherchera à déterminer avec l'algorithme des kPPV

    Sorties : 
        - data_base_with_distance : table (tableau de dictionnaires)
        copie de characters_data_base à laquelle on a ajouté à 
        chaque dictionnaire la clef 'Distance' qui correspond à
        la distance euclidienne entre ce personnage et
        le personnage cible new_character
        
        
        
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
        
    '''
    data_base_with_distance = characters_data_base
    n = len(characters_data_base)
    
    for i in range(0, n - 1):
        distance = sqrt((new_character['Courage'] + characters_data_base[i]['Courage']**2) 
                        + (new_character['Ambition'] + characters_data_base[i]['Ambition']**2)
                        + (new_character['Intelligence'] + characters_data_base[i]['Intelligence']**2)
                        + (new_character['Good'] + characters_data_base[i]['Good']**2))
        data_base_with_distance[i]['Distance'] = distance
    # Préconditions :
    assert type(characters_data_base) == list, \
           "La base de donnée être une liste de dictionnaires."
    
    for character in characters_data_base:
        assert type(character) == dict, \
               "La base de donnée doit être une liste de dictionnaires."
    
    data_base_with_distance = characters_data_base.copy()
    # Cette partie ajoutera la clef 'Distance' à chaque dictionnaire de table_with_distance
    return data_base_with_distance
    
    
# Importation de la table "Characters.csv" :
with open("Characters.csv", mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    characters_tab = [{key : value.replace('\xa0', ' ') for key, \
                       value in element.items()} for element in reader]


# Importation de la table "Caracteristiques_des_persos.csv" :
with open("Caracteristiques_des_persos.csv", mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    characteristics_tab = [{key : value for key, value in element.items()} \
                           for element in reader]
    
    
# Jointure de ces deux tables dans la table poudlard_characters :
poudlard_characters = []

for poudlard_character in characteristics_tab:
    for kaggle_character in characters_tab:
        if poudlard_character['Name'] == kaggle_character['Name']:
            poudlard_character.update(kaggle_character)
            poudlard_characters.append(poudlard_character)
'''
La table poudlard_characters est maintenant une liste de dictionnaires
où chaque dictionnaire  correspond à un personnage,
avec comme clefs toutes les informations que l'on a sur ce personnage
(dont la maison, le courage, l'ambition, l'intelligence, la tendance au bien)
'''
