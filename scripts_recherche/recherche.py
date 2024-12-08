"recherche.py contient des fonctions permettant de rechercher des éléments sur IMDB via l'API imdb"
from imdb import * # Importer l'API imdb
from imdb._exceptions import IMDbDataAccessError
from urllib.error import URLError
from tkinter import messagebox
from tkinter import ttk
from tkinter import Tk
from cache import * # Importer cache.py pour gérer les caches
from scripts_recherche.progression import *
from threading import Thread
from .notifications_recherche import afficher_notification # Importer la fonciton afficher_notification depuis le module notifications_recherche





cache = IMDBCache() # Créer un cache pour réduire les appels redondants à l'API IMDB
explorateur = Cinemagoer() # Objet Cinemagoer permettant d'explorer IMDB via l'API


def rechercher(requete:str, maitre=None|Tk, classemaitre=None,  barre=None|ttk.Progressbar) -> list:
    """Recherche le contenu de requete sur IMDB et met à jour la barre de progression barre
    - requete : élément à rechercher
    - maitre: widget maître de la barre de progression
    - classemaitre: classe spécifique du widget maitre, optionnel
    - barre: la barre de progression à mettre à jour"""

    # Assertions
    assert isinstance(requete, str), "requete doit être une chaîne de caractères"

    liste_resultats = [] # Liste des résultats trouvés pour la requête

    # Algorithme de recherhe ci-dessous


    films = explorateur.search_movie(requete) # Films contenant la requête dans leur titre
   

    #personnages = explorateur.search_character(requete) # Personnages de films contenant la requête dans leur nom

    #personnes = explorateur.search_person(requete) # Personnes ayant la requête dans leur nom



    resultats = 0
    for film in films: # Pour chaque film trouvé
        try: # Tenter de récupérer les infos du film depuis le cache
            id_film = film.movieID # Récupérer l'ID du film
            infos_film = cache.obtenir(id_film) # Obtenir les infos du film stockées dans le cache grâce à son ID
            if not infos_film: # Si les informations n'ont pas pu être récupérées depuis le cache
                infos_film = explorateur.get_movie(id_film) # Récupérer les informations en utilisant l'explorateur
                cache.ajouter_modifier(id_film, infos_film) # Ajouter l'ID et les infos du film dans le cache

            titre = infos_film["title"] # Récupérer le titre du film
            realisateurs = [dir["name"] for dir in infos_film["directors"]] # Récupérer le(s) réalisateur(s) du film
            #print(f"Réalisateur(s) : {"".join(realisateurs)}")
            annee = infos_film["year"] # Récupérer l'année de sortie du film

            #print(f"Titre : {titre}, Réalisateur(s) : {"".join(realisateurs)}, Année : {annee} ")   

            liste_resultats.append((titre, "".join(realisateurs), annee)) # Ajouter le film à la liste des résultats 

            resultats = len(liste_resultats)

            print(f"Traitement de {resultats} résultats.")
            #if isinstance(maitre, Tk) and isinstance(barre, ttk.Progressbar) or isinstance(maitre, classemaitre) and isinstance(barre, ttk.Progressbar): # Si on doit mettre à jour une barre de progression pour indiquer le stade de la recherche
            #    Thread(target=lambda:afficher_progression(maitre, barre, liste_resultats)).start() # Mettre à jour la barre de progression


        

        except IMDbDataAccessError: # En cas d'erreur de connection à IMDB
            messagebox.showerror("""Erreur de connexion avec IMDB", "Impossible de se connecter à IMDB. \n
                                  -  Il se peut que le site soit inaccessible quand bien même votre connexionn est effective (panne serveur, etc),
                                  - Il se peut aussi que votre connexion réseau soit défaillante. Essayez de vous reconnecter puis réessayez.""")
            return liste_resultats # Si des résultats on quand même été trouvés, les renvoyer

        except URLError as e: # En cas de connection générale
            #print(f"Erreur durant le traitement des résultats de recherche : {str(e)}") 
            messagebox.showerror("Erreur : connexion internet défaillante", "Impossible de se connecter à Internet. Vérifiez l'état de votre connexion et réessayez.")
            continue


        except KeyError: # En cas d'erreur de clé introuvable
            continue

        
        

    #for personnage in personnages: # Pour chaque personnage de film trouvé    
    #   liste_resultats.append(personnage) # Ajouter le personnage à la liste des résultats

    #for personne in personnes: # Pour chaque personne trouvée
    #    liste_resultats.append(personne) # Ajouter la personne à la liste des résultats    

    
    #print(f"Résultats trouvés : {liste_resultats}")
    print("Recherche terminée !")
    if not maitre.focus_get(): # Si l'application maître n'a pas le focus
        afficher_notification(titre="Recherche terminée !", message=f"movieDB a terminé la recherche pour {requete}.") # Envoyer une notification à l'utilisateur pour indiquer que la recherche est terminée
    return liste_resultats # Renvoyer la liste des résultats trouvés
    
