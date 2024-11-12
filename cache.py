"cache.py implémente une classe IMDBCache qui permet de réduire les appels redondants à l'API IMDB"
import threading # Importer threading pour gérer les threads
from functools import lru_cache # Importer la fonction lru_cache depuis functools


class IMDBCache:
    def __init__(self):
        "Instance de cache IMDB"
        self.contenu = {} # Contenu du cache
        self.lock = threading.Lock() # Créer un objet Lock pour verouiller les threads

    def obtenir(self, id_film):
        """Obtenir un film présent dans le cache
        - id_film : ID IMDB du film"""
        with self.lock: # On n'utilise qu'un seul thread
            if id_film in self.contenu: # si l'ID du film est présent dans le contenu du cache
                return self.contenu[id_film] # Retourner le film correspondant
            
            else: # Sinon
                return None # Ne rien renvoyer
            
    def ajouter_modifier(self, id_film, infos):
        """Ajoute / modifie les infos d'un film dans le cache.
        - id_film : ID du film dont on  ajoute / modifie les infos,
        - infos: Infos ajoutées / modifiées concernant le film"""
        
        with self.lock: # On n'utilise qu'un seul thread
            self.contenu[id_film] = infos # Mettre à jour le contenu du cache

        return self.contenu  # Renvoyer le contenu mis à jour    