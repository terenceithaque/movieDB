"recherche.py contient des fonctions permettant de rechercher des éléments sur IMDB via l'API imdb"
from imdb import * # Importer l'API imdb


explorateur = Cinemagoer() # Objet Cinemagoer permettant d'explorer IMDB via l'API


def rechercher(requete:str) -> list:
    "Recherche le contenu de requete sur IMDB"

    # Assertions
    assert isinstance(requete, str), "requete doit être une chaîne de caractères"

    liste_resultats = [] # Liste des résultats trouvés pour la requête

    # Algorithme de recherhe ci-dessous

    films = explorateur.search_movie(requete) # Films contenant la requête dans leur titre

    #personnages = explorateur.search_character(requete) # Personnages de films contenant la requête dans leur nom

    #personnes = explorateur.search_person(requete) # Personnes ayant la requête dans leur nom


    for film in films: # Pour chaque film trouvé
        id_film = film.movieID # ID IMDB du film
        infos_film = explorateur.get_movie(id_film) # Récupérer les infos sur le film (réalisateur(s), date,...)

        try: # Essayer de récupérer le(s) réalisateur(s), titre et année du film
            titre = infos_film["title"]
            realisateurs = ",".join(dir["name"] for dir in infos_film["directors"])
            annee = infos_film["year"]
            print(f"Titre : {titre}, Realisateurs : {"".join(realisateurs)}, Année : {annee}")
            liste_resultats.append((titre, realisateurs, annee)) # Ajouter le film à la liste des résultats
        
        except: # En cas d'erreur
            continue # Passer au résultat suivant

    #for personnage in personnages: # Pour chaque personnage de film trouvé    
    #   liste_resultats.append(personnage) # Ajouter le personnage à la liste des résultats

    #for personne in personnes: # Pour chaque personne trouvée
    #    liste_resultats.append(personne) # Ajouter la personne à la liste des résultats    

    
    print(f"Résultats trouvés : {liste_resultats}")
    return liste_resultats # Renvoyer la liste des résultats trouvés
    
