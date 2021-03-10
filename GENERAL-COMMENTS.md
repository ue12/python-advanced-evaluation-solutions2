- [commentaires communs à plusieurs étudiants](#commentaires-communs-à-plusieurs-étudiants)
  - [conception / réutilisabilité](#conception--réutilisabilité)
    - [structure de données](#structure-de-données)
    - [découpage](#découpage)
  - [efficacité / performances](#efficacité--performances)
    - [priority queue](#priority-queue)
    - [choix de la distance](#choix-de-la-distance)
  - [bugs fréquents](#bugs-fréquents)
    - [reachability](#reachability)
    - [JSON](#json)
  - [forme / style de codage](#forme--style-de-codage)

# commentaires communs à plusieurs étudiants

## conception / réutilisabilité

### structure de données

* il y avait plusieurs choix raisonnables pour représenter l'état d'un jeu
  * une simple liste de nombres entre 0 et 8
  * une liste de 3 listes de nombres
  * un tableau numpy de forme (3, 3)
* du coup on aurait apprécié une discussion sur la structure choisie;
  clairement la seconde ne présente presque que des inconvénients,
  la dernière est la plus compacte en mémoire mais paradoxalement ne se prête pas bien
  au calcul de la distance
* pour les plus avancés, ça vous donne un critère pour juger de votre travail;
  idéalement vous pouvez remplacer une implémentation par une autre en ne changeant **que
  le code de la classe `Board`*, dans l'idéal les autres classes ne sont pas du tout
  impactées si vous êtes partis sur un tableau numpy et que vous changez d'idée après coup
  parce que les performances sont décevantes

### découpage

en termes de conception réutilisable, l'énoncé vous invitait à réfléchir à un découpage du code

une façon (il y en a plein d'autres bien entendu) de s'y prendre consistait à définir

* une classe `Board` qui représente **uniquement** l'état du jeu; sans la notion de
  *comment on en est arrivé là*, juste où sont les pièces; c'est là typiquement qu'on peut
  implémenter
  * le critère d'atteignabilité
  * la logique qui énumère les boards voisins, ainsi que la transformation en
    texte dans les deux sens, lecture et écriture
  * les détails de la gestion du trou qui peut prendre plusieurs formes (0, - ou espace),
    c'est le genre de détails sordides qu'on veut confiner à un seul endroit du code
* une classe `State` qui, littéralement comme exposé dans l'énoncé, contient un board, une
  priorité, et un board précédent pour la tracabilité (reconstituer la chaine une fois la
  position cible atteinte)
* une classe `Solver` qui crée la *priority queue* - qui elle même contient des `State` -
  et principalement implémente l'algorithme principal

en termes de choix de répartition en modules (fichiers), l'énoncé insistait sur la
présence de **plusieurs fichiers**; les critères pour choisir :

* faire en sorte qu'on puisse utiliser la classe `Board` toute seule, pour implémenter,
  par exemple, une interface graphique de jeu de taquin sans intelligence; ça ferait du
  sens de la mettre dans `board.py`
* c'est raisonnable - mais pas obligatoire - de grouper les classes `State` et `Solver`
  dans un seul fichier car elles marchent ensemble, et *a priori* on n'a pas vraiment
  besoin de créer des objets `State` en dehors de la classe `Solver`
* du coup faire en sorte que `cli.py` soit le plus petit possible; logiquement ça ne fait
  que
  * lire les arguments de la ligne de commande (on utilise argparse pour ça d'habitude)
  * lire le fichier d'entrée
  * créer un objet `Solver` et lui faire un ou quelques appels de méthodes
  * et produire le fichier de sortie

## efficacité / performances

### priority queue

* le principal goulot d'étranglement dans l'algorithme, c'est le fait de garder la
  priority queue triée correctement; une approche naïve qui consiste à retrier la queue à
  chaque coup rend l'approche à la limite de l'utilisable
* pour ceux qui n'ont pas saisi les allusions de l'énoncé (et ses compléments), il fallait
  clairement ici utiliser le module `heapq` de la librairie standard, qui est bien
  optimisé pour le traitement d'une *priority queue*; ce qui confirme l'intérêt d'une
  classe `State`, sur laquelle on redéfinit l'ordre à utiliser dans le tri, grâce à une
  dunder méthode `__lt__`

### choix de la distance

* le sujet consistait aussi à justifer l'emploi d'une distance plutôt que l'autre;
  clairement manhattan est très supérieure à hamming, mais on s'attendait à en trouver
  une justification même intuitive
* par exemple pour les plus avancés on aurait pu s'attendre à un code où le changement de
  distance puisse se faire sans changer le code (une option sur la ligne de commande par
  exemple) - ou très peu (une variable globale quelque part);
  c'est très utile en pratique de pouvoir changer ce type de paramètres
  sans avoir à changer le code

## bugs fréquents

### reachability

tout le monde a bien vu le rapport avec la parité de la permutation;

l'invariant qu'il fallait voir pour bien comprendre, c'est qu'à chaque mouvement:

* la parité de la permutation change (puisqu'on ajoute **exactement une** transposition)
* ***et dans le même temps*** le trou change de couleur dans le damier (si vous peignez
  mentalement les cases en noir et blanc)

ce qui prouve donc que

* si le trou est au centre ou sur une diagonale (même couleur que la position de départ),
  la permutation est paire
* sinon c-a-d si le trou est sur un des bords, la permutation est impaire

il se trouve que, **parce que la largeur de la grille est impaire**, et de manière plutôt
coincidentelle, on peut se contenter de calculer la parité de la permutation sur les
tuiles (c'est-à-dire en ignorant le trou)

### JSON

manifestement pas mal de confusion autour du format JSON qui était demandé

```python
# plusieurs d'entre vous ont écrit quelque chose comme
output.write(str(record))
# pour produire du JSON il fallait faire plutôt
import json
output.write(json.dumps(record))
```

## forme / style de codage

* les commentaires: laissez un espace après le #

  ```python
  #ne collez pas le texte à gauche, c'est moche
  # laissez le respirer qu'on puisse bien le lire
  ```

* on recommande de coder en anglais, ce sera lisible par plus de monde

* pour énumérer les mouvements possibles, certains ont produit un code de plusieurs pages qui énumere les différentes possibilités; il **ne faut pas faire comme ça** !

  on peut éviter les codes super longs en faisant
  juste

  ```python
  for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0)):
      # essayer de déplacer le trou de dx, dy
      ...
  ```

  on pouvait aussi optimiser un peu en préparant à l'avance, une fois pour toutes, un dictionnaire qui associe

  *case -> cases voisines*

* pour le code de `cli.py`, on préconise en général d'éviter le code au *toplevel*

  c'est à dire que plutôt que de faire par exemple

  ```python
  import sys
  from board import Board

  in_filename, out_filename = sys.arg[1:3]
  board = Board.read_from_file(in_filename)
  if board.solvable():
     ...
  else:
     ...
  ```

  on préfère faire

  ```python
  import sys
  from board import Board

  def main():
      in_filename, out_filename = sys.arg[1:3]
      board = Board.read_from_file(in_filename)
      if board.solvable():
          ...
      else:
          ...

  main()
  ```
