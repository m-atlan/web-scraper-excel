"""
=====================================================
  SURVEILLANCE DES PRIX - Interface graphique
=====================================================
Une fenetre, un bouton. Le client ne voit jamais de code.

Lancement : python3 app_extraction.py
"""

import subprocess
import sys
import threading
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import ttk
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

# ---- REGLAGES ------------------------------------------------
TAUX_EURO = 1.17
NB_PAGES_MAX = 50
# --------------------------------------------------------------

BASE = "https://books.toscrape.com/catalogue/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36"}
NOTES = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


# =========================================================
#  PARTIE 1 : le travail (identique au script d'avant)
# =========================================================

def extraire_produits(soup, url_page):
    produits = []

    for carte in soup.select("article.product_pod"):
        prix = float(
            carte.select_one("p.price_color").text
            .replace("£", "").replace("Â", "").strip()
        )
        produits.append({
            "Titre": carte.h3.a["title"],
            "Prix (£)": prix,
            "Prix (€)": round(prix * TAUX_EURO, 2),
            "Note client": NOTES.get(carte.select_one("p.star-rating")["class"][1], 0),
            "Disponibilite": carte.select_one("p.instock").text.strip(),
            "Image": urljoin(url_page, carte.img["src"]),
            "Lien": urljoin(url_page, carte.h3.a["href"]),
        })

    return produits


def lancer_extraction(signaler):
    """
    'signaler' est une fonction que l'on appelle pour afficher
    l'avancement dans la fenetre. On separe le travail de l'affichage :
    la logique ne sait pas qu'une interface existe.
    """
    tous = []

    for numero in range(1, NB_PAGES_MAX + 1):
        url = f"{BASE}page-{numero}.html"
        try:
            reponse = requests.get(url, headers=HEADERS, timeout=15)
        except requests.RequestException:
            raise RuntimeError("Connexion internet impossible.")

        if reponse.status_code != 200:
            break

        tous.extend(extraire_produits(BeautifulSoup(reponse.text, "html.parser"), url))
        signaler(f"Page {numero} — {len(tous)} produits", numero / NB_PAGES_MAX * 100)

    if not tous:
        raise RuntimeError("Aucun produit trouve. Le site a peut-etre change.")

    df = pd.DataFrame(tous).drop_duplicates(subset="Lien").sort_values("Prix (€)", ascending=False)
    fichier = Path(f"catalogue_concurrent_{date.today():%Y-%m-%d}.xlsx").resolve()

    with pd.ExcelWriter(fichier, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Catalogue")
        feuille = writer.sheets["Catalogue"]
        for colonne in feuille.columns:
            largeur = max((len(str(c.value)) for c in colonne if c.value), default=10)
            feuille.column_dimensions[colonne[0].column_letter].width = min(largeur + 3, 55)
        feuille.freeze_panes = "A2"
        feuille.auto_filter.ref = feuille.dimensions

    return df, fichier


# =========================================================
#  PARTIE 2 : la fenetre
# =========================================================

class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Surveillance des prix")
        self.geometry("460x300")
        self.resizable(False, False)
        self.configure(bg="white")
        self.fichier = None

        tk.Label(self, text="Surveillance des prix",
                 font=("Helvetica", 19, "bold"), bg="white").pack(pady=(28, 2))
        tk.Label(self, text="Catalogue du site concurrent",
                 font=("Helvetica", 12), fg="#666", bg="white").pack()

        self.bouton = tk.Button(self, text="Lancer l'extraction",
                                font=("Helvetica", 14, "bold"),
                                command=self.demarrer,
                                height=2, width=20)
        self.bouton.pack(pady=22)

        self.barre = ttk.Progressbar(self, length=340, mode="determinate")
        self.barre.pack()

        self.message = tk.Label(self, text="Pret.", font=("Helvetica", 11),
                                fg="#666", bg="white")
        self.message.pack(pady=12)

    # --- affichage -------------------------------------------------

    def signaler(self, texte, pourcentage=None):
        """Met a jour la fenetre. Appelee depuis le fil de travail."""
        self.message.config(text=texte, fg="#666")
        if pourcentage is not None:
            self.barre["value"] = pourcentage
        self.update_idletasks()

    # --- actions ---------------------------------------------------

    def demarrer(self):
        self.bouton.config(state="disabled", text="Extraction en cours...")
        self.barre["value"] = 0
        # On travaille dans un fil separe, sinon la fenetre se fige
        # completement pendant la minute que dure l'extraction.
        threading.Thread(target=self.travailler, daemon=True).start()

    def travailler(self):
        try:
            df, fichier = lancer_extraction(self.signaler)
        except Exception as erreur:
            self.signaler(f"Erreur : {erreur}")
            self.message.config(fg="#c00")
            self.bouton.config(state="normal", text="Reessayer")
            return

        self.fichier = fichier
        self.barre["value"] = 100
        self.message.config(text=f"Termine — {len(df)} produits enregistres", fg="#080")
        self.bouton.config(state="normal", text="Ouvrir le fichier Excel",
                           command=self.ouvrir)

    def ouvrir(self):
        """Ouvre le fichier avec le logiciel par defaut, sur Mac comme sur Windows."""
        if sys.platform == "darwin":
            subprocess.run(["open", self.fichier])
        elif sys.platform == "win32":
            subprocess.run(["cmd", "/c", "start", "", str(self.fichier)], shell=False)
        else:
            subprocess.run(["xdg-open", self.fichier])


if __name__ == "__main__":
    Application().mainloop()