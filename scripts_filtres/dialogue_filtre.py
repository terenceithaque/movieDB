"dialogue_filtre.py contient une fonction demander_filtre qui demande à l'utilisateur de saisir un filtre"
from tkinter import simpledialog # Importer simpledialog depuis tkinter

def demander_filtre(type="Filtre", texte="Saisissez un filtre:"):
    """Demande un filtre à l'utilisateur avec texte comme demande. Si acun filtre n'est entré, renvoie une chaîne de caractères vide."""
    filtre = simpledialog.askstring(title=type, prompt=texte) # Demander un filtre à l'utilisateur et en renvoyer la valeur
    if not filtre: # Si l'utilisateur n'a pas saisi de filtre
        filtre = "" # Alors on considère que le filtre est une chaîne de caractères vide

    return filtre    