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
from csv import DictReader
from math import sqrt

# Constantes :
CARACTERISTICS = ('Courage', 'Ambition', 'Intelligence', 'Good')
    
# Définition des fonctions :
def euclidian_distance(character1: dict, character2: dict, caracteristics=CARACTERISTICS) -> float:
    '''
    Cette fonction calcule la distance entre deux personnages, en utilisant 
    la formule de la distance euclidienne.
    Cela nous servira pour l'algorithme des kPPV.
    
    Entrées :
        - character1 et character2 : dictionnaires qui correspondent chacun 
        à un personnage avec comme clefs au minimum 'Courage', 'Ambition', 
        'Intelligence' et 'Good'
        - caracteristics : tuple des caracteristiques qui nous
        permettent de calculer la distance ; 
        valeur par défaut : la constante CARACTERISTICS
    
    Sorties :
        - flottant, distance euclidienne entre ces deux personnages
    '''
    # Préconditions :        
    assert type(caracteristics) == tuple or type(caracteristics) == list, \
        "Les caractéristiques doivent être données \
        sous forme de tuple ou de liste."
        
    for character in (character1, character2):
        assert type(character) == dict, \
            "La base de donnée doit être une liste de dictionnaires."
        for caracteristic in caracteristics:
            assert caracteristic in character, \
                "Chaque personnage/dictionnaire doit contenir comme clefs \
                toutes les caractéristiques avec lesquelles \
                on veut calculer la distance."
        
    # Sortie :
    return sqrt(sum([(character1[key] - character2[key])**2 for key in caracteristics]))

def knn_house(characters_data_base: list, new_character: dict, caracteristics: tuple, k=3) -> str:
    '''
    Cette fonction renvoie la maison du nouveau personnage, 
    définie avec l'algorithme des kPPV.
    
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
        - new_character_house : chaîne de caractères, maison prévue
        - k_nn : table, (tableau de dictionnaires) contenant les k plus proches
        voisins du nouveau personnage, sous forme de dictionnaires.

    '''
    # Préconditions :
    assert type(caracteristics) == tuple or type(caracteristics) == list, \
        "Les caractéristiques doivent être données \
        sous forme de tuple ou de liste."
        
    assert type(characters_data_base) == list, \
           "La base de donnée être une liste de dictionnaires."
    
    for character in characters_data_base:        
        assert type(character) == dict, \
               "La base de donnée doit être une liste de dictionnaires."               
        for caracteristic in caracteristics:
            assert caracteristic in character, \
                "Chaque personnage/dictionnaire doit contenir comme clefs \
                toutes les caractéristiques avec lesquelles \
                on veut calculer la distance."
            
    assert type(new_character) == dict, \
           "Le nouveau personnage doit être sous forme de dictionnaire."
           
    for caracteristic in caracteristics:
        assert caracteristic in new_character, \
            "Chaque personnage/dictionnaire doit contenir comme clefs \
            toutes les caractéristiques avec lesquelles \
            on veut calculer la distance."
    
    
    
    data_base_with_distance = [character.update({'Distance': euclidian_distance(character, new_character)}) for character in characters_data_base]
    # Cette partie ajoutera la clef 'Distance' à chaque dictionnaire de table_with_distance

    
    return data_base_with_distance


# Importation de la table "Characters.csv" :
with open("Characters.csv", mode='r', encoding='utf-8') as f:
    reader = DictReader(f, delimiter=';')
    characters_tab = [{key : value.replace('\xa0', ' ') for key, \
                       value in element.items()} for element in reader]


# Importation de la table "Caracteristiques_des_persos.csv" :
with open("Caracteristiques_des_persos.csv", mode='r', encoding='utf-8') as f:
    reader = DictReader(f, delimiter=';')
    characteristics_tab = [{key : value for key, value in element.items()} \
                           for element in reader]
    
    
# Jointure de ces deux tables dans la table poudlard_characters :
poudlard_characters = []

for poudlard_character in characteristics_tab:
    for kaggle_character in characters_tab:
        if poudlard_character['Name'] == kaggle_character['Name']:
            poudlard_character.update(kaggle_character)
            
            # On transforme les caractéristiques en entiers
            for caracteristic in CARACTERISTICS:
                poudlard_character[caracteristic] = int(poudlard_character[caracteristic])
                
            poudlard_characters.append(poudlard_character)
'''
La table poudlard_characters est maintenant une liste de dictionnaires
où chaque dictionnaire  correspond à un personnage,
avec comme clefs toutes les informations que l'on a sur ce personnage
(dont la maison, le courage, l'ambition, l'intelligence, la tendance au bien)
'''
