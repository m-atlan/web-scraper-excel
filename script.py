"""
=====================================================
  SURVEILLANCE DES PRIX - Librairie Marchand
=====================================================
Extrait le catalogue du site concurrent et genere un
fichier Excel avec les prix en livres et en euros.

Realise par Mordi A.
"""

import sys
import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ---- REGLAGES MODIFIABLES PAR LE CLIENT ----------------------
TAUX_EURO = 1.17        # taux livre -> euro, a ajuster si besoin
NB_PAGES_MAX = 50       # tout le catalogue
# --------------------------------------------------------------

BASE = "https://books.toscrape.com/catalogue/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}
NOTES = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def attendre():
    """Garde la fenetre ouverte apres un double-clic (sans planter si lance en automatique)."""
    try:
        input("\nAppuyez sur Entree pour fermer cette fenetre...")
    except EOFError:
        pass


def recuperer_page(numero, live=True):
    if live:
        try:
            reponse = requests.get(f"{BASE}page-{numero}.html", headers=HEADERS, timeout=15)
        except requests.RequestException:
            return None
        if reponse.status_code != 200:
            return None
        html = reponse.text
    else:
        fichier = Path("site_test") / f"page-{numero}.html"
        if not fichier.exists():
            return None
        html = fichier.read_text(encoding="utf-8")

    return BeautifulSoup(html, "html.parser")


def extraire_produits(soup):
    produits = []

    for carte in soup.select("article.product_pod"):
        prix_livres = float(
            carte.select_one("p.price_color").text
            .replace("£", "").replace("Â", "").strip()
        )

        produits.append({
            "Titre": carte.h3.a["title"],
            "Prix (£)": prix_livres,
            "Prix (€)": round(prix_livres * TAUX_EURO, 2),   # <- demande du client
            "Note client": NOTES.get(carte.select_one("p.star-rating")["class"][1], 0),
            "Disponibilite": carte.select_one("p.instock").text.strip(),
            "Lien": BASE + carte.h3.a["href"].replace("../", ""),
            "Image": urljoin(BASE, carte.img["src"]),
        })

    return produits


def scraper(live=True):
    tous = []

    for numero in range(1, NB_PAGES_MAX + 1):
        soup = recuperer_page(numero, live=live)
        if soup is None:
            break

        tous.extend(extraire_produits(soup))
        print(f"  Page {numero} analysee... ({len(tous)} produits)")

        if live:
            time.sleep(0.4)

    return tous


def exporter(produits):
    df = pd.DataFrame(produits)
    df = df.drop_duplicates(subset="Lien").sort_values("Prix (€)", ascending=False)

    # Le nom du fichier contient la date : le client garde un historique
    # sans rien faire, et peut comparer d'une semaine sur l'autre.
    fichier = f"catalogue_concurrent_{date.today():%Y-%m-%d}.xlsx"

    with pd.ExcelWriter(fichier, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Catalogue")
        feuille = writer.sheets["Catalogue"]

        for colonne in feuille.columns:
            largeur = max((len(str(c.value)) for c in colonne if c.value), default=10)
            feuille.column_dimensions[colonne[0].column_letter].width = min(largeur + 3, 55)

        feuille.freeze_panes = "A2"
        feuille.auto_filter.ref = feuille.dimensions   # filtres cliquables sur l'en-tete

    return df, fichier


if __name__ == "__main__":
    live = "--test" not in sys.argv

    print("=" * 52)
    print("  SURVEILLANCE DES PRIX - Librairie Marchand")
    print("=" * 52)
    print("\nRecuperation du catalogue en cours...\n")

    produits = scraper(live=live)

    if not produits:
        print("\n[ERREUR] Impossible de recuperer les donnees.")
        print("Verifiez votre connexion internet, puis relancez.")
        print("Si le probleme persiste, contactez-moi.")
        attendre()
        sys.exit(1)

    df, fichier = exporter(produits)

    print("\n" + "=" * 52)
    print(f"  TERMINE : {len(df)} produits enregistres")
    print("=" * 52)
    print(f"\nFichier cree : {fichier}")
    print(f"  Prix moyen : {df['Prix (€)'].mean():.2f} EUR")
    print(f"  En stock   : {(df['Disponibilite'] == 'In stock').sum()} sur {len(df)}")

    # Sans cette pause, la fenetre se ferme instantanement au double-clic
    # et le client ne voit rien. Detail minuscule, impact enorme.
    attendre()
