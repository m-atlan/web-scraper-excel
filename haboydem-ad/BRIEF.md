# Pub Haboydem : brief et instructions

Ce dossier contient deux publicités pour **הבוידעם** (https://haboydem.co.il), un jeu quotidien en hébreu, et tout ce qu'il faut pour les modifier et refaire le rendu.

## Le jeu en trois lignes

- 7 questions par jour, les mêmes pour tout le monde, 30 secondes par question.
- Chaque question a beaucoup de bonnes réponses. Plus la réponse est rare, plus elle rapporte.
- L'échelle va du commun au rare : השולחן 10, המקרר 20, המגירה 30, הממ״ד 60, המחסן 85, הבוידעם 100.

## L'idée de la pub

**Même question, deux joueurs, deux réponses. Celui qui sort la réponse la plus rare gagne.**

Le spectateur doit comprendre la règle sans qu'on la lui explique : il voit un joueur répondre l'évidence (תפוז, 10 points) et l'autre sortir la réponse que personne ne trouve (אתרוג, 100 points). La phrase de fin est « בואו לשחק בבוידעם ».

## Contenu du dossier

| Fichier | Rôle |
| --- | --- |
| `haboydem-duel.mp4` | La pub vidéo finale : 23 s, 1080×1920 (9:16), 30 i/s, sans son |
| `duel.html` | La source de la vidéo : animation jouable dans un navigateur |
| `render.js` | Script qui transforme `duel.html` en MP4, image par image |
| `gsap.min.js` | Bibliothèque d'animation GSAP 3.12.5, en local |
| `index.html` | Une deuxième pub, interactive : on tire la corde du boydem et on joue une manche d'essai |

## Déroulé de la vidéo (`duel.html`)

| Temps | Plan |
| --- | --- |
| 0,0 – 2,6 s | Carton d'accroche : « אותה שאלה. שני שחקנים. מי ישלוף תשובה נדירה יותר? » |
| 2,6 – 4,2 s | Dézoom sur la table vue du dessus, deux téléphones (נועם à droite, עומר à gauche), question « פרי הדר » |
| 4,2 – 8,3 s | Zoom sur נועם : il tape « תפוז », envoie, tampon « 10 · השולחן » |
| 8,3 – 12,5 s | Travelling vers עומר : il tape « אתרוג », tampon jaune « 100 · הבוידעם », éclat |
| 12,5 – 17,2 s | Dézoom, étiquettes de score, manche 2 (drapeau à trois couleurs) : איטליה 20, ליטא 85 |
| 17,2 – 19,0 s | Victoire de עומר, 185 contre 30, « נדיר יותר = יותר נקודות » |
| 19,0 – 23,2 s | Carton de fin : plaque « הבוידעם », « בואו לשחק בבוידעם », haboydem.co.il |

## Comment c'est construit

- La scène fait 540×960 et s'adapte à la fenêtre. Le rendu la capture à l'échelle 2, donc 1080×1920.
- `#world` est la table. La caméra est la fonction `cam(cx, cy, échelle)` : elle déplace et agrandit `#world` en entier pour zoomer sur un point.
- Toute l'animation est une seule timeline GSAP, en bas de `duel.html`, découpée par des commentaires `/* ---- 3.1 round 1 ---- */` avec les temps en secondes.
- Les fonctions utiles : `cap(texte, début, fin)` pour une légende, `tap(joueur, y, temps)` pour un appui du doigt, `play(joueur, manche, temps, scoreTotal)` pour une réponse complète (appui, frappe, envoi, tampon, score).
- Le contenu (questions, réponses, points, prénoms) est dans les tableaux `ROUNDS` et `P` en haut du script.
- Rien ne dépend de l'horloge : chaque image est calculée à partir du temps de la timeline, donc le rendu est identique à chaque fois.

## Identité visuelle (reprise du site)

- Polices : **Suez One** pour les titres et les chiffres, **Heebo** pour le texte (Google Fonts).
- Couleurs : mur `#F3EAD6`, papier `#FBF6EC`, encre `#2A1E17`, bleu canard `#1D5A62`, jaune de la plaque `#E9B93F`, bois `#C58A54`.
- Style : illustration à contour épais, ombres pleines décalées, bouts de papier légèrement penchés. Pas de dégradés brillants ni de 3D.
- Tout le texte est en hébreu, de droite à gauche.

## Refaire le rendu

Il faut Node.js, Playwright (avec Chromium) et ffmpeg.

```
node render.js            # écrit out/haboydem-duel.mp4
node render.js mon/dossier
```

Pour seulement prévisualiser, ouvrir `duel.html` dans un navigateur : l'animation démarre toute seule, et un bouton permet de la relancer.

## Ce qui est provisoire

- **Les points sont inventés.** La question du drapeau vient du site, mais les scores (10, 100, 20, 85) sont des exemples. À remplacer par de vraies données du jeu si possible.
- Les prénoms נועם et עומר sont des exemples.
- Il n'y a ni musique, ni voix off, ni bruitages.

## Pistes d'amélioration

1. Ajouter le son : musique légère, « clic » à chaque appui, son de tampon, petite fanfare sur le 100.
2. Ajouter une voix off en hébreu sur l'accroche et sur la phrase de fin.
3. Remplacer les téléphones dessinés par de vraies captures de l'écran de jeu, et reprendre les illustrations du site (la porte, le paillasson, la plante).
4. Dessiner de vraies mains plutôt que des doigts en forme de capsule.
5. Afficher un clavier pendant la frappe et le chronomètre de 30 secondes qui se vide.
6. Faire une version courte de 10 à 15 secondes (une seule manche) et un format carré 1:1.
7. Donner plus de présence à la victoire : confettis, le téléphone gagnant qui se soulève, le score qui grossit.

## À ne pas changer

- L'idée centrale : la réponse rare bat la réponse évidente.
- La phrase de fin « בואו לשחק בבוידעם » et l'adresse haboydem.co.il.
- Les couleurs et les deux polices du site.
