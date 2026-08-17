# web-scraper-excel

Outil de veille tarifaire : il parcourt le catalogue en ligne d'un concurrent,
récupère chaque produit, et génère un fichier Excel prêt à l'emploi avec les
prix convertis en euros.

Pensé pour être utilisable **sans connaissances techniques** : on lance le
script, il affiche sa progression, et il dépose un fichier `.xlsx` daté à côté
de lui.

## Ce que contient le fichier généré

Un onglet `Catalogue`, une ligne par produit, avec :

| Colonne | Contenu |
|---|---|
| Titre | nom du produit |
| Prix (£) | prix affiché sur le site source |
| Prix (€) | prix converti selon le taux configuré |
| Note client | note sur 5 |
| Disponibilité | état du stock |
| Lien | URL de la fiche produit |
| Image | URL de la photo |

Les lignes sont triées du plus cher au moins cher, les doublons sont retirés,
la largeur des colonnes est ajustée, l'en-tête est figé et les filtres
automatiques sont activés.

Le nom du fichier contient la date du jour
(`catalogue_concurrent_2026-08-16.xlsx`) : en relançant l'outil chaque semaine,
on constitue un historique sans rien avoir à faire, et on peut comparer
l'évolution des prix d'une semaine sur l'autre.

## Installation

Python 3.9 ou plus récent est requis.

```bash
python -m venv .venv
source .venv/bin/activate        # sous Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation

```bash
python script.py
```

Le fichier Excel apparaît dans le dossier courant. Un mode hors ligne est
disponible pour tester sans accès internet, à partir de pages HTML placées dans
un dossier `site_test/` :

```bash
python script.py --test
```

## Réglages

Les deux paramètres modifiables se trouvent en haut de `script.py`, dans un
bloc identifié :

```python
TAUX_EURO = 1.17        # taux livre -> euro, à ajuster si besoin
NB_PAGES_MAX = 50       # nombre maximum de pages à parcourir
```

## Note sur le site source

La démonstration cible <https://books.toscrape.com>, un site public conçu
spécifiquement pour l'apprentissage et les tests d'extraction de données.
Avant de viser un autre site, vérifiez ses conditions d'utilisation et son
fichier `robots.txt`.

---

Réalisé par Mordi A.
