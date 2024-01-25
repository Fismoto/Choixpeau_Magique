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

TESTS_PROFILES = ({'Courage': 9, 'Ambition': 2, 'Intelligence': 8, 'Good': 9},\
                  {'Courage': 6, 'Ambition': 7, 'Intelligence': 9, 'Good': 7},\
                  {'Courage': 3, 'Ambition': 8, 'Intelligence': 6, 'Good': 3},\
                  {'Courage': 2, 'Ambition': 3, 'Intelligence': 7, 'Good': 8},\
                  {'Courage': 3, 'Ambition': 4, 'Intelligence': 8, 'Good': 8})
    
# Définition des fonctions :
def euclidian_distance(character1: dict, character2: dict, caracteristics=CARACTERISTICS) -> float:
    '''
    Cette fonction calcule la distance entre deux personnages, en utilisant 
    la formule de la distance euclidienne.
    Cela nous servira pour l'algorithme des kPPV.
    
    Entrées :
        - caracteristics : tuple des caracteristiques qui nous
        permettent de calculer la distance 
        valeur par défaut : la constante CARACTERISTICS
        - character1 et character2 : dictionnaires qui correspondent chacun 
        à un personnage avec comme clefs au minimum 
        tous les éléments de caracteristics

    
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


def knn_house(characters_data_base: list, new_character: dict, caracteristics: tuple, k=5) -> str:
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
        (dont au moins tous les éléments de caracteristics)
        Note : on ne connait pas la maison de ce personnage cible,
        c'est ce que l'on cherchera à déterminer avec l'algorithme des kPPV

    Sorties : 
        - new_character_house : chaîne de caractères, 
        maison prévue du nouveau personnage
        - neighbors : liste de tuples correspondant 
        chacun l'un des k plus proches voisins de new_character 
        et contenant chacun deux éléments : 
            - un dictionnaire, l'un des k plus proches voisins 
            du nouveau personnage
            - un flottant, la distance entre ce même dictionnaire 
            et le nouveau personnage.
        Note : ce tableau est trié par distance croissante
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
    
    list_of_distances = [(index, euclidian_distance(new_character, character)) for index, character in enumerate(characters_data_base)]
    list_of_distances.sort(key=lambda character: character[1])
    k_nearest_neighbors = [(characters_data_base[index], distance) for index, distance in list_of_distances[:k]]
    
    houses_of_neighbors = {'Slytherin': 0, 'Griffindor': 0, 'Ravenclaw': 0, \
                           'Hufflepuf': 0}
    
    for neighbor, distance in k_nearest_neighbors :
        
        if neighbor['House'] == 'Slytherin' :
            houses_of_neighbors['Slytherin'] += 1
            
        elif neighbor['House'] == 'Griffindor' :
            houses_of_neighbors['Griffindor'] += 1
            
        elif neighbor['House'] == 'Ravenclaw' :
            houses_of_neighbors['Ravenclaw'] += 1
            
        else :
            houses_of_neighbors['Hufflepuf'] += 1
    
    houses_of_neighbors = sorted(houses_of_neighbors.items(), key = lambda house : house[1])
    houses_of_neighbors.reverse()
    
    

    
    
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


for profile in TESTS_PROFILES:
    print(knn_house(poudlard_characters, profile, CARACTERISTICS, k=5))