"Script principal de l'application"
from tkinter import * # Importer le module tkinter pour l'interface graphique
from tkinter import ttk
from imdb import Cinemagoer # Importer Cinemagoer depuis l'API imdb
from recherche import * # Importer le module recherche qui contient les fonctions de recherche sur IMDB

class Application(Tk):
    def __init__(self):
        "Instance de l'application"
        super().__init__() # Hériter des attributs de la classe Tk de tkinter
        self.title("movieDB - Votre base de données cinéphile") # Titre de la fenêtre principale de l'application

        self.label_recherche = Label(self, text="Rechercher un film, un acteur, etc... :") # Libellé pour indiquer à l'utilisateur quels genres de choses il peut rechercher
        self.label_recherche.pack()
        self.barre_recherche = Entry(self) # Barre de recherche
        self.barre_recherche.pack(fill="x")

        self.bouton_rechercher = Button(self, text="Rechercher !", command=self.afficher_resultats_recherche) # Bouton pour recherher le(s) terme(s) entrés dans la barre de recherche et afficher les résultats
        self.bouton_rechercher.pack()

        # Définir les colonnes pour l'arbre visuel des résultats de recherche
        self.colonnes = ("titres_noms")
        
        # Créer un abre visuel de résultats de recherche
        self.arbre_resultats = ttk.Treeview(self, columns=self.colonnes, show="headings")
        # Définition des en-têtes de l'abre visuel
        self.arbre_resultats.heading("titres_noms", text="Titres / noms")

        self.arbre_resultats.pack(fill="both")


    def afficher_resultats_recherche(self):
        "Afficher les résultats de recherche"
        #self.arbre_resultats.delete("1.0", END)
        resultats_recheche = rechercher(self.barre_recherche.get()) # Rechercher dans IMDB les éléments qui correspondent à la requête entrée dans la barre de recherche
        if len(resultats_recheche) > 0: # Si des résultats de recherche ont été trouvés 
            for element in resultats_recheche: # Pour chaque résultat de recherche
                self.arbre_resultats.insert("", END, values=element) # Ajouter le résultat à l'arbre de résultats

        else: # Sinon
            self.arbre_resultats.insert(parent="", index="end", text="Oups ! Pas de résultats de recherche.")
            



app = Application() # Créer une instance de l'application
app.mainloop() # Lancer la boucle principale de la fenêtre        
