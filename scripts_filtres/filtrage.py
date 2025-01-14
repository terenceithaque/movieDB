"filtrage.py gère les opération de filtrage de recherches"
#from imdb import *

def filtrer(liste:list, filtre:str, respect_casse=False) -> list:
    """Renvoie une copie de liste filtrée avec filtre. \n
        Exemple d'utilisation:\n
        ma_liste = ["Hello", "world", "!"] \n
        print(filtrer(ma_liste, "Hello")) \n
        ['Hello'] \n\n
        - liste: la liste d'éléments à filtrer
        - filtre: une chaîne de caractères contenant le filtre à utiliser
        - respect_casse : un booléen, mis sur False par défaut. Si activé (mis à True), le filtrage tient strictement compte de la casse. Dans tous les autres cas, la casse n'est pas prise en compte.
        """
    liste_filtree = [] # Liste filtrée, vide pour l'instant

    filtre = str(filtre) # S'assurer que le filtre est sous forme de chaîne de caractères

    for element in liste: # Pour chaque élément de la liste non filtrée
        element_str = str(element) # S'assurer que l'élément est sous forme de chaîne de caractères
        if respect_casse: # Si on doit respecter la casse
            if filtre.lower().strip() in element_str.lower().strip() or element_str.lower().strip() == filtre.lower().strip(): # Si le filtre est compris dans l'élément ou que l'élément lui-même est le filtre
                #print(f"'{filtre}' dans {element} ou  {filtre}={element} ")
                liste_filtree.append(element) # Ajouter l'élément à la liste filtrée

            

        else: # Si on ne doit pas tenir compte de la casse
            if filtre.lower().strip() in element_str.lower().strip() or filtre.upper().strip() in element_str.upper().strip() or element_str == filtre: 
                #print(f"{filtre} dans {element} ou  {filtre}={element} ")
                liste_filtree.append(element)
            
                



    return liste_filtree        



