# coding: utf_8

'''
Codé par : Octave FORTUN, Milo MONTAGNE, Pierrick LEFEVRE

Projet NSI 3 kPPV, partie I "Harry se fait (enfin) la malle"

Le programme utilise l'algorithme des k plus proches voisins pour attribuer 
une maison à un personnage en fonction de 4 caractéristiques 
(le courage, l'ambition, l'intelligence, la tendance au bien)
à l'aide d'une base de données de personnages d'Harry Potter

Licence : CC-BY-NC-SA

github : https://github.com/Nodd20/Projet_malle_Gr2
'''

# Importation des modules :
import csv


# Définition des fonctions :
def distance(table, character):
    '''
    Cette fonction renvoie la table avec la clef 'Distance'
    ajoutée à chaque dictionnaire.
    La valeur de cette clef est la distance entre le character (personnage type)
    et le personnage symbolisé par le dictionnaire.
    '''
    table_with_distance = table
    # Cette partie ajoutera la clef 'Distance' à chaque dictionnaire de table_with_distance
    return table_with_distance
    
    
# Importation des informations (seule la maison nous intéresse) des personnages dans une table :
with open("Characters.csv", mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    characters_tab = [{key : value.replace('\xa0', ' ') for key, \
                       value in element.items()} for element in reader]


# Importation des caractéristiques (le courage, l'ambition, l'intelligence, la tendance au bien) des personnages dans une table :
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
avec comme clefs toutes les informations qu'on a sur ce personnage
(dont la maison, le courage, l'ambition, l'intelligence, la tendance au bien)
'''

