"Script principal de l'application"
from tkinter import * # Importer le module tkinter pour l'interface graphique
from tkinter import ttk
from imdb import Cinemagoer # Importer Cinemagoer depuis l'API imdb
from recherche import * # Importer le module recherche qui contient les fonctions de recherche sur IMDB
from scripts_filtres.filtrage import * # Importer le module filtrage, qui contient des fonctions pour appliquer des filtres de recherche, depuis le dossier scripts_filtres
from scripts_filtres.dialogue_filtre import * # Importer le module dialogue_filtre depuis le dossier scripts_filtres afin de pouvoir demander à l'utilisateur de saisir des filtres
import threading

class Application(Tk):
    def __init__(self):
        "Instance de l'application"
        super().__init__() # Hériter des attributs de la classe Tk de tkinter
        self.title("movieDB - Votre base de données cinéphile") # Titre de la fenêtre principale de l'application

        self.barre_menus = Menu(self, tearoff=None) # Barre de menus principale de l'application
        self.menu_fichier = Menu(self.barre_menus, title="Fichier") # Créer un menu "Fichier"
        self.menu_fichier.add_command(label="Quitter...", command=self.destroy) # Bouton pour quitter l'application

        self.barre_menus.add_cascade(label="Fichier", menu=self.menu_fichier)

        self.menu_tri_filtres = Menu(self.barre_menus, tearoff=0) # Menu pour les options de tri et de filtre
        self.sous_menu_tri = Menu(self.menu_tri_filtres, tearoff=0) # Menu pour les options de tri
        self.menu_tri_filtres.add_cascade(label="Tri...", menu=self.sous_menu_tri)
        self.sous_menu_filtres = Menu(self.menu_tri_filtres, tearoff=0) # Menu pour les options de filtre

        self.sous_menu_filtres.add_command(label="Titre...", command=lambda:self.filtrer_resultats(type_filtre="titre")) # Commande de filtrage par titre
        self.sous_menu_filtres.add_command(label="Réalisateur(s)...", command=lambda:self.filtrer_resultats(type_filtre="réalisateur(s)")) # Commande de filtrage par réalisateur(s)
        self.sous_menu_filtres.add_command(label="Année...", command=lambda:self.filtrer_resultats(type_filtre="année")) # Commande de filtrage par année de sortie

        self.menu_tri_filtres.add_cascade(label="Filtres...", menu=self.sous_menu_filtres)

        
        self.barre_menus.add_cascade(label="Tri & filtres", menu=self.menu_tri_filtres) # Ajouter le menu Tri & filtres à la barre de menus
        self.config(menu=self.barre_menus)


        

        self.label_recherche = Label(self, text="Rechercher un film, un acteur, etc... :") # Libellé pour indiquer à l'utilisateur quels genres de choses il peut rechercher
        self.label_recherche.pack()
        self.barre_recherche = Entry(self) # Barre de recherche
        self.barre_recherche.pack(fill="x")

        self.bouton_rechercher = Button(self, text="Rechercher !", command=lambda:threading.Thread(target=self.afficher_resultats_recherche).start()) # Bouton pour recherher le(s) terme(s) entrés dans la barre de recherche et afficher les résultats
                                                                                                                                                      # La méthode est appelée dans un nouveau thread pour éviter le blocage de la fenêtre 
        self.bouton_rechercher.pack()                                                                                                                  


        self.label_statut_recherche = Label(self, text="Aucune recherche") # Libellé indiquant le statut de la recherche
        self.label_statut_recherche.pack()
        self.resultats_affiches = 0 # Nombre de résultats affichés dans l'arbre visuel

        self.resultats_recherche = [] # Liste des résultats de recherche, vide pour l'instant

        # Définir les colonnes pour l'arbre visuel des résultats de recherche
        self.colonnes = ("titre", "réalisateur", "année")
        
        # Créer un abre visuel de résultats de recherche
        self.arbre_resultats = ttk.Treeview(self, columns=self.colonnes, show="headings")
        # Définition des en-têtes de l'abre visuel
        self.arbre_resultats.heading("titre", text="Titre")
        self.arbre_resultats.heading("réalisateur", text="Réalisateur(s)")
        self.arbre_resultats.heading("année", text="Année de sortie")

        self.arbre_resultats.pack(fill="both")


    def afficher_resultats_recherche(self):
        "Afficher les résultats de recherche"
        #self.arbre_resultats.delete("1.0", END)
        # Effacer les résultats de recherche précédents


        self.label_statut_recherche.config(text="Recherche en cours. Cela peut prendre un peu de temps...")
        

        for resultat in self.arbre_resultats.get_children():
            self.arbre_resultats.delete(resultat)
            self.resultats_affiches -= 1 # Réduire le nombre résultats affichés

        self.arbre_resultats.insert("", END, values="".join("Recherche en cours..."))
        self.arbre_resultats.update() # Mettre à jour l'arbre pour afficher le texte
        self.resultats_recheche = rechercher(self.barre_recherche.get()) # Rechercher dans IMDB les éléments qui correspondent à la requête entrée dans la barre de recherche
        items = self.arbre_resultats.get_children() # Obtenir les items présents dans l'arbre visuel
        for item in items: # Supprimer les items
            self.arbre_resultats.delete(item)
        
        if len(self.resultats_recheche) > 0: # Si des résultats de recherche ont été trouvés 
            for resultat in self.resultats_recheche: # Pour chaque résultat de recherche
                self.arbre_resultats.insert("", END, values=resultat) # Ajouter le résultat à l'arbre de résultats
                self.resultats_affiches += 1 # Augmenter le nombre de résultats affichés

        else: # Sinon
            self.arbre_resultats.insert(parent="", index="end", text="Oups ! Pas de résultats de recherche.")


        self.label_statut_recherche.config(text=f"{self.resultats_affiches} résultats affichés sur {len(self.resultats_recheche)}")    
            


    def filtrer_resultats(self, type_filtre=None | str):
        "Demande un filtre à l'utilisateur et effectue un filtrage des données affichées dans l'arbre visuel en fonction de la saisie"
        if self.resultats_recheche: # Si des résultats de recherche ont été trouvés
            if not type_filtre: # Si le type du filtre n'est pas précisé
                filtre = demander_filtre(type="Filtre", texte=f"Saisissez un filtre")

            else: # Sinon
                filtre = demander_filtre(type= f"Filtre de type {type_filtre}", texte=f"Saisissez un filtre de type {type_filtre}...")


            resultats_filtres = filtrer(self.resultats_recheche, filtre) # Filtrer les résultats de recherche avec le filtre saisi
            for resultat in self.arbre_resultats.get_children(): # Pour chaque résultat présent dans l'arbre visuel
                if not resultat in resultats_filtres: # Si le résultat ne fait pas partie des résultats filtrés
                    self.arbre_resultats.delete(resultat)   
                    self.resultats_affiches -= 1
                    self.label_statut_recherche.config(text=f"{self.resultats_affiches} résultats affichés sur {len(self.resultats_recheche)}")


            for resultat in resultats_filtres: # Pour chaque résultat correspondant au filtre
                self.arbre_resultats.insert("", END, values=resultat) # Ajouter le résultat à l'arbre visuel  
                self.resultats_affiches += 1

                

        self.label_statut_recherche.config(text=f"{self.resultats_affiches} résultats affichés sur {len(self.resultats_recheche)}")
        self.arbre_resultats.update() # Mettre à jour l'arbre visuel            


app = Application() # Créer une instance de l'application
app.mainloop() # Lancer la boucle principale de la fenêtre        
