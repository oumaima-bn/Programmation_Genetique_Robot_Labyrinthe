# Robot mobile dans un labyrinthe 7×7 — Programmation génétique

Projet réalisé par **Oumaima Bendjaj**
Université Ibn Tofail — Département d'Informatique

---

## 📌 Description

Ce projet simule un robot mobile qui évolue dans un labyrinthe de taille 7×7 généré aléatoirement. Le robot dispose de trois capteurs (devant, gauche, droite) lui permettant de détecter les murs autour de lui, et doit trouver le chemin vers la sortie.

La stratégie de déplacement n'est pas programmée à la main : elle est **découverte automatiquement** grâce à un algorithme génétique, une technique d'intelligence artificielle inspirée de la sélection naturelle.

## 🎯 Objectifs

- Explorer un labyrinthe 7×7
- Utiliser des capteurs locaux (mur / libre)
- Apprendre une stratégie de déplacement par évolution
- Trouver un chemin vers la sortie
- Optimiser le nombre de déplacements

## 🧰 Technologies

- **Python 3**
- [`pyamaze`](https://pypi.org/project/pyamaze/) — génération et affichage du labyrinthe
- Bibliothèque standard : `random`

## ⚙️ Installation

```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd <nom-du-depot>

# 2. Installer la dépendance
pip install pyamaze
```

> `pyamaze` utilise `tkinter` pour l'affichage. Il est installé par défaut avec Python sous Windows et macOS ; sous Linux : `sudo apt install python3-tk`.

## ▶️ Utilisation

```bash
python programmation_genetique_robot_labyrinthe.py
```

Le programme :
1. génère un labyrinthe aléatoire,
2. fait évoluer une population de stratégies,
3. affiche dans la console le meilleur score de chaque génération,
4. si une solution est trouvée, ouvre une fenêtre avec le chemin tracé du robot.

Exemple de sortie console :

```
Generation 0 | Best score = -120
Generation 1 | Best score = -60
...
Generation 12 | Best score = 1744
✅ Solution trouvée !
```

Si aucune solution n'est trouvée après toutes les générations, le message `Aucune solution complète trouvée` s'affiche. Il suffit alors de relancer le programme (voir [Limites](#-limites-et-pistes-damélioration)).

## 🧬 Fonctionnement de l'algorithme

### 1. Représentation d'un individu

Chaque individu est une liste de **12 entiers** représentant une stratégie. Chaque valeur est une action :

| Valeur | Action |
|:------:|--------|
| `0` | Avancer |
| `1` | Tourner à gauche |
| `2` | Tourner à droite |

### 2. Capteurs

Le robot lit trois capteurs binaires `(devant, gauche, droite)`, ce qui donne **8 situations possibles**. La situation est convertie en indice :

```
indice = devant × 4 + gauche × 2 + droite
action = individu[indice]
```

### 3. Fonction de fitness

Chaque individu est simulé sur 50 pas maximum depuis la case de départ `(1, 1)`. La simulation s'arrête si le robot revient sur une case déjà visitée ou atteint la sortie `(7, 7)`.

```
score = 300 − 30 × distance_Manhattan_à_la_sortie − 2 × nombre_de_pas
score += 1500   si la sortie est atteinte
```

Le score favorise donc les robots qui **se rapprochent de la sortie** et qui y arrivent **rapidement**.

### 4. Opérateurs génétiques

| Étape | Méthode |
|-------|---------|
| **Initialisation** | 100 individus aléatoires |
| **Sélection** | Les 20 % meilleurs individus (top 20 %) deviennent parents |
| **Croisement** | Croisement à un point de coupure aléatoire entre deux parents |
| **Mutation** | 40 % de chance qu'un gène d'un individu soit modifié aléatoirement |

### 5. Boucle principale

```
Initialisation → [ Évaluation → Sélection → Croisement → Mutation ] × générations
```

L'algorithme s'arrête dès qu'un individu obtient un score **> 1400** (c'est-à-dire qu'il a atteint la sortie), ou après 100 générations.

## 🔧 Paramètres modifiables

Définis au début du fichier :

| Paramètre | Valeur par défaut | Rôle |
|-----------|:-----------------:|------|
| `r, c` | `7, 7` | Dimensions du labyrinthe |
| `POP_SIZE` | `100` | Taille de la population |
| `GENERATIONS` | `100` | Nombre maximum de générations |
| `MAX_STEPS` | `50` | Nombre maximum de pas par simulation |
| `loopPercent` | `30` | Pourcentage de boucles dans le labyrinthe (plusieurs chemins possibles) |

## 📊 Résultats

Le système est capable, dans de nombreux cas, de trouver une stratégie permettant au robot d'atteindre la sortie. Les résultats ne sont toutefois pas garantis : la programmation génétique est une méthode **probabiliste** qui dépend de l'initialisation aléatoire et de la forme du labyrinthe généré.

Exemple de chemin trouvé par le robot (en bleu) dans un labyrinthe 7×7 :

![Chemin trouvé par le robot dans le labyrinthe](images/resultat_labyrinthe.jpg)

## ⚠️ Limites et pistes d'amélioration

- Le robot démarre toujours en `(1, 1)` ; pour atteindre l'objectif « quel que soit le point de départ », il faudrait évaluer chaque individu sur plusieurs positions de départ.
- Les actions « gauche » / « droite » correspondent à des déplacements dans des directions fixes de la grille et non à une rotation relative à l'orientation du robot. Introduire une orientation (cap) rendrait la simulation plus réaliste.
- Seules 8 cases sur 12 du génome sont utilisées (8 combinaisons de capteurs possibles) ; réduire le génome à 8 gènes serait plus cohérent.
- Ajouter l'**élitisme** (conserver les meilleurs individus tels quels) et une graine aléatoire (`random.seed`) pour obtenir des résultats reproductibles.
- Comparer avec des algorithmes classiques (BFS, A*) pour mesurer l'optimalité du chemin trouvé.

