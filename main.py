"Script principal de l'application"
from tkinter import * # Importer le module tkinter pour l'interface graphique
from tkinter import ttk
from tkinter import messagebox
from imdb import Cinemagoer # Importer Cinemagoer depuis l'API imdb
from scripts_recherche.recherche import * # Importer le module recherche qui contient les fonctions de recherche sur IMDB
from scripts_filtres.filtrage import * # Importer le module filtrage, qui contient des fonctions pour appliquer des filtres de recherche, depuis le dossier scripts_filtres
from scripts_filtres.dialogue_filtre import * # Importer le module dialogue_filtre depuis le dossier scripts_filtres afin de pouvoir demander à l'utilisateur de saisir des filtres
import threading
from itertools import chain


def arbre_en_dict(arbre:ttk.Treeview) -> dict:    
    """Renvoie un dictionnaire reflétant le contenu d'un arbre visuel.
    - arbre : l'arbre visuel à convertir en dictionnaire"""
    # Assertions
    assert isinstance(arbre, ttk.Treeview), "L'arbre visuel doit être un objet ttk.Treeview"

    titres_colonnes = arbre["columns"] # Obtenir les colonnes de l'arbre sous forme de liste
    colonnes_donnees = {col : [] for col in titres_colonnes} # Dictionnaire contenant le titre des colonnes et leur contenu sous forme de liste
            

            # Remplir le dicitionnaire avec les éléments de l'arbre visuel
    for element in arbre.get_children(): 
            valeurs = arbre.item(element, "values")
            for i, col in enumerate(titres_colonnes): # Pour chaque colonne
                colonnes_donnees[col].append(str(valeurs[i]))  # Ajouter les valeurs correspondantes à la liste représentant son contenu
    
    return colonnes_donnees # Retourner le contenu de l'arbre sous forme de dictionnaire


class Application(Tk):
    def __init__(self):
        "Instance de l'application"
        super().__init__() # Hériter des attributs de la classe Tk de tkinter
        self.title("movieDB - Votre base de données cinéphile") # Titre de la fenêtre principale de l'application

        self.barre_menus = Menu(self, tearoff=None) # Barre de menus principale de l'application
        self.menu_fichier = Menu(self.barre_menus, title="Fichier") # Créer un menu "Fichier"
        self.menu_fichier.add_command(label="Quitter...", command=self.quitter) # Bouton pour quitter l'application

        self.barre_menus.add_cascade(label="Fichier", menu=self.menu_fichier)

        self.menu_afficher = Menu(self.barre_menus, title="Afficher") # Créer un menu "Afficher"
        self.menu_afficher.add_checkbutton(label="Tout", command=lambda:self.afficher_colonne([0, 1, 2]), state="active") # Commande pour afficher tout
        self.menu_afficher.add_checkbutton(label="Titre", command=lambda:self.afficher_colonne(0)) # Commande pour afficher les titres seulement
        self.menu_afficher.add_checkbutton(label="Réalisateur(s)", command=lambda:self.afficher_colonne(1)) # Commande pour afficher uniquement le(s) réalisateur(s)
        self.menu_afficher.add_checkbutton(label="Année", command=lambda:self.afficher_colonne(2)) # Commande pour afficher l'année uniquement

        self.barre_menus.add_cascade(label="Afficher", menu=self.menu_afficher)


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

        #self.barre_recherche.bind("<Return>", self.afficher_resultats_recherche)                                                                                                         


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

        self.contenu_arbre = {} # Dictionnaire vide représentant le contenu de l'arbre visuel







    def afficher_resultats_recherche(self, event=None):
        "Afficher les résultats de recherche"
        #self.arbre_resultats.delete("1.0", END)
        # Effacer les résultats de recherche précédents


        self.protocol("WM_DELETE_WINDOW", self.quitter)
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
                self.label_statut_recherche.config(text=f"{self.resultats_affiches} résultats affichés sur {len(self.resultats_recheche)}")    
                
                

        else: # Sinon
            self.label_statut_recherche.config(text="Aucun résultat trouvé. Essayez d'autres termes de recherche.")


        self.contenu_arbre = arbre_en_dict(self.arbre_resultats) # Mettre à jour le dictionnaire représentant le contenu de l'arbre visuel
        
        
        



    def afficher_colonne(self, index=int|list):
        """Affiche seulement les éléments d'une colonne dont l'indice est spécifié, dans l'arbre visuel.
        - index : un entier ou une liste d'entiers (pour afficher plusieurs colonnes)"""

        # Assertions
        assert isinstance(index, int) or isinstance(index, list), "index doit être un entier ou une liste d'entiers" # Vérifier que index est un entier ou une liste d'entiers

        titres_colonnes = self.arbre_resultats["columns"]
        if type(index).__name__ == "int": # Si l'indice est un entier seul
            assert index <= len(self.contenu_arbre), f"L'indice doit être inférieur ou égal à {len(self.contenu_arbre)}"
            print(f"Contenu de l'arbre visuel : {self.contenu_arbre}")


            # Tout d'abord, restaurer le contenu original de l'arbre visuel afin de ne pas le perdre
            
            


            valeurs_col = self.contenu_arbre[titres_colonnes[index]] # Extraire les valeurs de la colonne à afficher
            print(f"Valeurs de la colonne : {valeurs_col}")
            for i, element in enumerate(valeurs_col): # Pour chaque élément de l'arbre visuel
                #print(f"Element : {element}")
                item = self.arbre_resultats.item(self.arbre_resultats.identify_element(index, i), "values")  # Elément converti en item
                item_liste = list(item) # Item converti sous forme de liste
                items_affiches = item_liste # Items affichés
                #print(str(item))
                for i, donnee in enumerate(item_liste): # Si l'item n'est pas présent dans les valeurs de la colonne à afficher
                    print(f"Donnée : {str(donnee)}")
                    for el in chain(self.contenu_arbre):
                        print(f"el : {el}")

                    if str(donnee) not in chain(*self.contenu_arbre) and len(valeurs_col) > 0:
                        items_affiches[i] = "" # Transformer les éléments à ne pas afficher en une chaîne vide
                        item = self.arbre_resultats.item(element, values=tuple(items_affiches)) # Actualiser l'item

                    else:
                        items_affiches[i] = str(donnee)
                        item = self.arbre_resultats.item(element, values=tuple(items_affiches))    

                #item_liste = list(item)        

                        

            
            self.arbre_resultats.update() # Mettre à jour l'arbre visuel 

        elif type(index).__name__ =="list": # Si plusieurs indices ont été fournis
            pass        

           






            


    def filtrer_resultats(self, type_filtre=None | str):
        "Demande un filtre à l'utilisateur et effectue un filtrage des données affichées dans l'arbre visuel en fonction de la saisie"
        if self.resultats_recheche: # Si des résultats de recherche ont été trouvés
            if not type_filtre: # Si le type du filtre n'est pas précisé
                filtre = demander_filtre(type="Filtre", texte=f"Saisissez un filtre")

            else: # Sinon
                filtre = demander_filtre(type= f"Filtre de type {type_filtre}", texte=f"Saisissez un filtre de type {type_filtre}...")


            resultats_filtres = filtrer(self.resultats_recheche, filtre) # Filtrer les résultats de recherche avec le filtre saisi
            print(f"Résultats correspondants au filtre '{filtre}' : {resultats_filtres}")
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


    def quitter(self, event=None):
        """Demande à l'utilisateur s'il souhaite quitter l'application"""
        # Demander confirmation à l'utilisateur
        quitter = messagebox.askyesno("Êtes-vous sûr(e) de quitter ?", "Quitter l'application annulera toute recherche en cours. Voulez-vous vraiment faire cela ?")

        if quitter: # Si l'utilisateur a confirmé qu'il veut quitter l'application
            self.destroy() # Détruire la fenêtre principale
        
        else: # Sinon
            return # Annuler l'arrêt


app = Application() # Créer une instance de l'application
app.mainloop() # Lancer la boucle principale de la fenêtre        
