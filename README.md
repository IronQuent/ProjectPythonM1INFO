# Analyse comparative de corpus

Cette analyse permet de comparer des mots ou groupe de mots issus de deux corpus différents.

## Installation

Fonctionne avec une version 3.8 de Python.

Installation du fichier "requirements.txt" sur macOs :

```bash
python -m pip install -r requirements.txt
```
Installation du fichier "requirements.txt" sur Windows :

```bash
py -m pip install -r requirements.txt
```

## Utilisation

Page Menu :
	- Comparaison de mots des corpus : Comparer les mots les plus fréquents dans les corpus
	- Recherche de mots dans les corpus : Rechercher un mot ou groupe de mot dans les corpus
Page Comparaison de mots des corpus :
	- Champ : taper le nombre de mots les plus fréquents à afficher
	- Analyser : lance l'analyse TFxIDF sur les corpus afin de retourner les mots les plus fréquents
	- Menu : retour au menu principal
Page Recherche de mots dans les corpus :
	- Champ : taper le mot ou groupe de mots a rechercher dans les corpus
	- Rechercher : lance la recherche dans les corpus et retourne le résultat sous la forme d'un affichage graphique
	- Menu : retour au menu principal