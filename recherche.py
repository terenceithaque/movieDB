"recherche.py contient des fonctions permettant de rechercher des éléments sur IMDB via l'API imdb"
from imdb import * # Importer l'API imdb
from cache import * # Importer cache.py pour gérer les caches


cache = IMDBCache() # Créer un cache pour réduire les appels redondants à l'API IMDB
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
        try: # Tenter de récupérer les infos du film depuis le cache
            id_film = film.movieID # Récupérer l'ID du film
            infos_film = cache.obtenir(id_film) # Obtenir les infos du film stockées dans le cache grâce à son ID
            if not infos_film: # Si les informations n'ont pas pu être récupérées depuis le cache
                infos_film = explorateur.get_movie(id_film) # Récupérer les informations en utilisant l'explorateur
                cache.ajouter_modifier(id_film, infos_film) # Ajouter l'ID et les infos du film dans le cache

            titre = infos_film["title"] # Récupérer le titre du film
            realisateurs = [dir["name"] for dir in infos_film["directors"]] # Récupérer le(s) réalisateur(s) du film
            annee = infos_film["year"] # Récupérer l'année de sortie du film

            #print(f"Titre : {titre}, Réalisateur(s) : {"".join(realisateurs)}, Année : {annee} ")   

            liste_resultats.append((titre, "".join(realisateurs), annee)) # Ajouter le film à la liste des résultats 


        except Exception as e: # En cas d'erreur
            print(f"Erreur durant le traitement des résultats de recherche : {str(e)}") 
            continue   

        """id_film = film.movieID # ID IMDB du film
        infos_film = explorateur.get_movie(id_film) # Récupérer les infos sur le film (réalisateur(s), date,...)

        try: # Essayer de récupérer le(s) réalisateur(s), titre et année du film
            titre = infos_film["title"]
            realisateurs = ",".join(dir["name"] for dir in infos_film["directors"])
            annee = infos_film["year"]
            print(f"Titre : {titre}, Realisateurs : {"".join(realisateurs)}, Année : {annee}")
            
        
        except: # En cas d'erreur
            continue # Passer au résultat suivant"""

    #for personnage in personnages: # Pour chaque personnage de film trouvé    
    #   liste_resultats.append(personnage) # Ajouter le personnage à la liste des résultats

    #for personne in personnes: # Pour chaque personne trouvée
    #    liste_resultats.append(personne) # Ajouter la personne à la liste des résultats    

    
    print(f"Résultats trouvés : {liste_resultats}")
    return liste_resultats # Renvoyer la liste des résultats trouvés
    
