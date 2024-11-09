"Script principal de l'application"
from tkinter import * # Importer le module tkinter pour l'interface graphique
from imdb import Cinemagoer # Importer Cinemagoer depuis l'API imdb


class Application(Tk):
    def __init__(self):
        "Instance de l'application"
        super().__init__() # Hériter des attributs de la classe Tk de tkinter
        self.title("movieDB - Votre base de données cinéphile") # Titre de la fenêtre principale de l'application



app = Application() # Créer une instance de l'application
app.mainloop() # Lancer la boucle principale de la fenêtre        
