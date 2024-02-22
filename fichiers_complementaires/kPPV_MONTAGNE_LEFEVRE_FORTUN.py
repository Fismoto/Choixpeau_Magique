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
from math import sqrt

# Constantes :
CARACTERISTICS = ('Courage', 'Ambition', 'Intelligence', 'Good')

TESTS_PROFILES = ({'Courage': 9, 'Ambition': 2, 'Intelligence': 8, 'Good': 9},\
                  {'Courage': 6, 'Ambition': 7, 'Intelligence': 9, 'Good': 7},\
                  {'Courage': 3, 'Ambition': 8, 'Intelligence': 6, 'Good': 3},\
                  {'Courage': 2, 'Ambition': 3, 'Intelligence': 7, 'Good': 8},\
                  {'Courage': 3, 'Ambition': 4, 'Intelligence': 8, 'Good': 8})
    
# Définition des fonctions :
def csv_dict_import(file_name: str) -> list:
    '''
    Importation d'une table à partir d'un fichier csv (utf-8)
    Entrée :
        - file_name, chaîne de cractère, chemin du fichier csv
    Sortie :
        - table, liste de dictionnaires
    '''
    # Précondition :
    assert type(file_name) == str, "Le nom du fichier doit être un str"

    table = []
    with open(file_name, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        key_line = lines[0].strip()
        keys = key_line.split(";")
        for line in lines[1:]:
            line = line.strip()
            values = line.split(';')
            dico = {}
            for i in range(len(keys)):
                dico[keys[i]] = values[i]
            table.append(dico)
        return table

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
        - caracteristics : tuple des caracteristiques qui nous
        	permettent de calculer la distance ; 
        	valeur par défaut : la constante CARACTERISTICS
            
        - characters_data_base : table (tableau de dictionnaires) 
        où chaque dictionnaire  correspond à un personnage,
        avec comme clefs toutes les informations qu'on a sur ce personnage
        (dont au moins 'House', 'Courage', 'Ambition', 'Intelligence', 'Good')

        - new_character : dictionnaire qui correspond à un personnage
        avec comme clefs les caractéristiques qu'on a sur ce personnage
        (dont au moins tous les éléments de caracteristics)
        Note : on ne connait pas la maison de ce personnage cible,
        c'est ce que l'on cherchera à déterminer avec l'algorithme des kPPV
        
		- k : entier, nombre de plus proches voisins pris en compte ; 
        valeur par défaut : 5

    Sorties : 
        - new_character_house : chaîne de caractères, 
        maison prévue du nouveau personnage
        - neighbors : liste de dictionnaires correspondant 
        chacun l'un des k plus proches voisins de new_character 
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
            
    assert type(k) == int and k > 0, "k doit être sous forme d'entier positif."
    
    assert k<= len(characters_data_base), \
        "k doit être plus petit que la longueur de la table."
    
    # Pour ne pas modifier de variable globale :
    data_base_changed = characters_data_base.copy()
    for i in range(len(data_base_changed)):
        data_base_changed[i]['Distance'] = euclidian_distance(new_character, \
                        data_base_changed[i], caracteristics=CARACTERISTICS)

    data_base_changed.sort(key=lambda character: character['Distance'])
    k_nearest_neighbors = data_base_changed[:k]
    
    houses_of_neighbors = {}
    
    for neighbor in k_nearest_neighbors :        
        if neighbor['House'] in houses_of_neighbors:
            houses_of_neighbors[neighbor['House']] += 1
        else:
            houses_of_neighbors[neighbor['House']] = 1
    
    items_houses_of_neighbors = sorted(houses_of_neighbors.items(), \
                                 key = lambda house: house[1])
    items_houses_of_neighbors.reverse()
    
    if len(items_houses_of_neighbors) == 1:
        return (items_houses_of_neighbors[0][0], k_nearest_neighbors)
        
    elif items_houses_of_neighbors[0][1] > items_houses_of_neighbors[1][1]:
        return (items_houses_of_neighbors[0][0], k_nearest_neighbors)
    
    else:
        for neighbor in k_nearest_neighbors:
            if neighbor['House'] in {items_houses_of_neighbors[0][0], \
                                     items_houses_of_neighbors[1][0]}:
                return (neighbor['House'], k_nearest_neighbors)
    # On ne gère pas les cas de triple égalité

def knn_str(profile : dict, neighbors : list, house : str) -> None:
    '''   
    Cette procédure affiche les caractéristiques du nouveau personnage,
    ses k plus proches voisins 
    (avec leurs caractéristiques, maisons et distance du nouveau personnage)
    et enfin affiche la maison retenue pour ce nouveau personnage.
    '''
    # Préconditions :
    assert house in {'Gryffindor', 'Ravenclaw', 'Slytherin', 'Hufflepuff'}, \
        "La maison retenue du personnage doit être une maison d'Harry Potter."
    assert type(profile) == dict, \
        "Le nouveau personnage doit être sous forme de dictionnaire."
     
    assert type(neighbors) == list, \
        "La base de donnée être une liste de dictionnaires."
    '''
    for neighbor in neighbors:        
        assert type(neighbor) == dict, \
            "La base de donnée doit être une liste de dictionnaires."               
        for caracteristic in caracteristics:
            assert caracteristic in neighbor, \
                "Chaque personnage/dictionnaire doit contenir comme clefs \
                    toutes les caractéristiques avec lesquelles \
                        on veut calculer la distance."
    '''
    assessment = f"\nLe personnage ayant les caractéristiques : {profile} a pour plus proches voisins : \n"

    for i in range(len(neighbors)):
        assessment += f"\t - {neighbors[i]['Name']}, de la maison {neighbors[i]['House']}, qui "\
              f"a une distance avec le personnage cible de : {round(neighbors[i]['Distance'], 3)}."
            
    assessment += f"\nFinalement, ce personnage cible ira dans la maison {house}.\n"

    return assessment


# Importation de la table "Characters.csv" :
characters_tab = csv_dict_import("fichiers_complementaires/Characters.csv")

# Importation de la table "Caracteristiques_des_persos.csv" :
characteristics_tab = csv_dict_import("fichiers_complementaires/Caracteristiques_des_persos.csv")
    
    
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
    house, k_n_neighbors = knn_house(poudlard_characters, profile, CARACTERISTICS, k=5)
    knn_str(profile, k_n_neighbors, house)

'''
response = input("\n \
                 \n Voulez-vous entrez vous-même des caractéristiques ? \
    (1 pour oui 2 pour non) : ")

while response == '1':
    try:
        k_client = int(input("Donner votre k : "))
        caracteristics_client = {}    
        for caracteristic in CARACTERISTICS:
            caracteristics_client[caracteristic] = int(input(f"\
                Valeur de la caractéristique {caracteristic} : "))
        house, k_n_neighbors = knn_house(poudlard_characters, caracteristics_client, CARACTERISTICS, k=k_client)
        knn_print(caracteristics_client, k_n_neighbors, house)
    except:
        print("Saisie incorrecte, désolé !!")
    
    response = input("\n \
                     \n Voulez-vous à nouveau entrez vous-même des caractéristiques ? \
                     (1 pour oui 2 pour non) : ")

print("Dommage, à une prochaîne fois !")
    
# Fin du programme
'''