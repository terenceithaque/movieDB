"tri.py permet d'effectuer des opérations de tri"


def tri_alphabetique(liste: list[str]) -> list[str]:
    "Effectue un tri par ordre alphabétique sur une liste de chaînes de caractère liste"
    return sorted(liste, key= lambda x: x.lower()) # Utiliser la fonction sorted sur la liste


def tri_anti_alphabetique(liste : list[str]) -> list[str]:
    "Effectue un tri par ordre anti-alphabétique sur une liste de chaînes de caractère liste"
    return sorted(liste, key= lambda x: x.lower())[::-1] # Trier la liste d'abord, puis l'inverser


def tri_croissant(liste : list[int]) -> list[int]:
    "Effectue un tri par ordre croissant sur une liste de nombres entiers liste"
    return sorted(liste, key= lambda x: x)


def tri_decroissant(liste : list[int]) -> list[int]:
    "Effectue un tri par ordre décroissant sur une liste de nombres entiers liste"
    return sorted(liste, key = lambda x: x)[::-1]

liste = [1, 9, 10, 17, 121]
liste = tri_decroissant(liste)
print(liste)

