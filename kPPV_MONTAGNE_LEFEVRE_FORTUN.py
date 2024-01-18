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
    for character in (character1, character2):
        assert type(character) == dict, \
            "La base de donnée doit être une liste de dictionnaires."
        for caracteristic in caracteristics:
            assert caracteristic in character, \
                "Chaque dictionnaire/personnage doit contenir comme clefs \
                toutes les caractéristiques avec lesquelles \
                on veut calculer la distance."
    
    assert type(caracteristics) == tuple or type(caracteristics) == list, \
        "Les caractéristiques doivent être données \
        sous forme de tuple ou de liste."
        
        
    return sqrt(sum([(character1[key] - character2[key])**2 for key in caracteristics]))

def knn(data, query_point, k=3):
    """K-nearest neighbors algorithm."""
    distances = [(index, euclidian_distance(query_point, item)) for index, item in enumerate(data)]
    sorted_distances = sorted(distances, key=lambda x: x[1])
    neighbors = [data[index] for index, _ in sorted_distances[:k]]
    return neighbors


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

def euclidian_distance(character1: dict, character2: dict) -> float:
    """Calculates the Euclidean distance between two points."""
    return sqrt(sum((character1[key] - character2[key]) ** 2 for key in ["Intelligence", "Good", "Ambition", "Courage"]))

def knn(data, query_point, k=3):
    """K-nearest neighbors algorithm."""
    distances = [(index, euclidian_distance(query_point, item)) for index, item in enumerate(data)]
    sorted_distances = sorted(distances, key=lambda x: x[1])
    neighbors = [data[index] for index, _ in sorted_distances[:k]]
    return neighbors

query_point = {'Intelligence': 8, 'Good': 8, 'Ambition': 8, 'Courage': 9}
result = knn(poudlard_characters, query_point, k=3)

# Afficher les voisins trouvés
for neighbor in result:
    print(f"Name: {neighbor['Name']}, Distance: {euclidian_distance(query_point, neighbor)}")