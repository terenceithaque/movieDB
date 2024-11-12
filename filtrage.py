"filtrage.py gère les opération de filtrage de recherches"
from imdb import *

def filtrer(liste:list, filtre:str) -> list:
    """Renvoie une copie de liste filtrée avec filtre. \n
        Exemple d'utilisation:
        ma_liste = ["Hello", "world", "!"] \n
        print(filtrer(ma_liste, "Hello"))
        ['Hello']
        """
    liste_filtree = [] # Liste filtrée, vide pour l'instant

    for element in liste: # Pour chaque élément de la liste non filtrée
        if filtre in element or element == filtre: # Si le filtre est compris dans l'élément ou que l'élément lui-même est le filtre
            liste_filtree.append(element) # Ajouter l'élément à la liste filtrée


    return liste_filtree        



