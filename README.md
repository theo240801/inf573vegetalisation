# inf573vegetalisation
Projet d'INF573 sur la détection et la classification de la végétalisation des villes

## Installation
- Cloner le repo
- Ajouter le fichier "images" de la clée USB fournie par le professeur et le renommer "data". Il doit contenir deux dossiers "rgb" et "ir'

## Explication de l'arborescence du projet
- "data" est le dossier qui contient les sous-dossier "rgb" et "ir" contenant eux-mêmes les images sur lesquelles nous faisons fonctionner le code. Il est dans le gitignore et doit donc être ajouté à la main.
- "doc" contient la bibliographie du projet


## Feuille de route
- combiner les images sattelites 
- trouver les composantes connexes des villes
- une fois qu'on a la composante connexe, trouver un indice représentant la couverture végétale

après:
- corréler cet indice à d'autres paramètres
- ?? patterns detection 
 -?? compter le nombre d'arbres 
- ??classifier les différents types de végétations (utiliser le CNN fourni)


## Idées d'amélioration
Commencer à implémenter le CNN
Objectif = ne pas compter l'herbe
+ pouvoir prendre en compte les arbres qui se font manger au threshold -> définir un threshold "par zone labellisée comme un arbre"
