"Script principal de l'application"
from tkinter import * # Importer le module tkinter pour l'interface graphique
from imdb import Cinemagoer # Importer Cinemagoer depuis l'API imdb


class Application(Tk):
    def __init__(self):
        "Instance de l'application"
        super().__init__() # Hériter des attributs de la classe Tk de tkinter
        self.title("movieDB - Votre base de données cinéphile") # Titre de la fenêtre principale de l'application

        self.label_recherche = Label(self, text="Rechercher un film, un acteur, etc... :") # Libellé pour indiquer à l'utilisateur quels genres de choses il peut rechercher
        self.label_recherche.pack()
        self.barre_recherche = Entry(self) # Barre de recherche
        self.barre_recherche.pack(fill="x")



app = Application() # Créer une instance de l'application
app.mainloop() # Lancer la boucle principale de la fenêtre        
