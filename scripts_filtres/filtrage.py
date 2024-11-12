"filtrage.py gère les opération de filtrage de recherches"
#from imdb import *

def filtrer(liste:list, filtre:str, respect_casse=False) -> list:
    """Renvoie une copie de liste filtrée avec filtre. \n
        Exemple d'utilisation:\n
        ma_liste = ["Hello", "world", "!"] \n
        print(filtrer(ma_liste, "Hello")) \n
        ['Hello']
        """
    liste_filtree = [] # Liste filtrée, vide pour l'instant

    for element in liste: # Pour chaque élément de la liste non filtrée
        if respect_casse: # Si on doit respecter la casse
            if str(filtre).lower() in str(element).lower() or str(element).lower() == str(filtre).lower(): # Si le filtre est compris dans l'élément ou que l'élément lui-même est le filtre
                liste_filtree.append(element) # Ajouter l'élément à la liste filtrée

        else: # Si on ne doit pas tenir compte de la casse
            if str(filtre).lower() in str(element) or str(filtre).upper() in str(element) or element == filtre: 
                liste_filtree.append(element)


    return liste_filtree        



