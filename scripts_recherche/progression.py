"progression.py permet d'afficher la progression d'une recherche"
from tkinter import Tk
from tkinter import ttk # Importer le module ttk de Tkinter
import time

def afficher_progression(maitre:Tk, barre:ttk.Progressbar, resultats_actuels:list):
    """Affiche la progression via le widget barre du widget maitre
    - maitre: Le widget  maître de la barre de progression
    - barre: La barre de progression 
    - resultats_actuels : Les résultats actuellement trouvés"""

    for i in range(len(resultats_actuels)): # Pour le nombre de résultats actuellement trouvés
        barre["value"] = i / len(resultats_actuels * 100) # Mettre à jour la barre de progression
        maitre.update_idletasks() # Mettre à jour l'interface graphique
        time.sleep(0.1) # Attendre 100 millisecondes
