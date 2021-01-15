#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 08:12:56 2020

@author: quentinthomasson
"""
#Librairies
import pickle
import Author
import re
import pandas
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize
import math
import numpy

#Classe corpus
class Corpus():
    #Constructeur
    def __init__(self,name):
        self.name = name
        self.collection = {}
        self.authors = {}
        self.id2doc = {}
        self.id2aut = {}
        self.ndoc = 0
        self.naut = 0
    
    #Ajout d'un doc au corpus
    def add_doc(self, doc):
        self.collection[self.ndoc] = doc
        self.id2doc[self.ndoc] = doc.get_title()
        self.ndoc += 1
        aut_name = doc.get_author()
        aut = self.get_aut2id(aut_name)
        if aut is not None:
            self.authors[aut].add(doc)
        else:
            self.add_aut(aut_name,doc)
    
    #Ajout d'auteur au corpus
    def add_aut(self, aut_name,doc):
        aut_temp = Author.Author(aut_name)
        aut_temp.add(doc)
        self.authors[self.naut] = aut_temp
        self.id2aut[self.naut] = aut_name
        self.naut += 1

    #Obtenir l'id d'un auteur
    def get_aut2id(self, author_name):
        aut2id = {v: k for k, v in self.id2aut.items()}
        heidi = aut2id.get(author_name)
        return heidi
    
    #Obtenir le document i
    def get_doc(self, i):
        return self.collection[i]
    
    #Obtenir le corpus
    def get_coll(self):
        return self.collection

    #Affichage
    def __str__(self):
        return "Corpus: " + self.name + ", Number of docs: "+ str(self.ndoc)+ ", Number of authors: "+ str(self.naut)
    
    #Représentation
    def __repr__(self):
        return self.name
    
    #Trier par titre le corpus
    def sort_title(self,nreturn=None):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_title())][:(nreturn)]
    
    #Trier par date le corpus
    def sort_date(self,nreturn):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_date(), reverse=True)][:(nreturn)]
    
    #Sauvegarder le corpus
    def save(self,file):
            pickle.dump(self, open(file, "wb" ))
            
    #Nettoyage du texte passé en paramètre
    def nettoyer_texte(self, chaineChar):
        #Passe la chaîne de caractère en minuscules
        chaineChar = chaineChar.lower()
        #Remplacer retour à la ligne
        chaineChar = chaineChar.replace("\n", " ")
        #Remplacer la ponctuation
        chaineChar =  re.sub(r'[^\w\s]', ' ', chaineChar)
        #Remplacer les chiffres
        chaineChar = re.sub('[0-9]', ' ', chaineChar)
        return chaineChar
    
    #Rechercher un mot dans le corpus, retourne la liste des documents contenant ce mot
    def search(self, word):
        list = []
        #Nettoyage du mot entré
        word = self.nettoyer_texte(word)
        #Si le mot entré est vide
        if (word.isspace() == True or not word):
            print("Mot non valide !")
        else:
            #Parcours du corpus
            for i in range (0, len(self.collection)):
                #Nettoyage du texte
                textClean = self.nettoyer_texte(self.collection[i].get_text())
                #Vérifie si le mot apparaît dans le texte du document
                if (len(re.findall(word, textClean)) > 0):
                    list.append(i)
            return list
    
    #Concordancier
    def concorde(self, word, lengthContext):
        list = self.search(word)
        #Création dataframe
        listConcord = pandas.DataFrame(columns=['contexte gauche', 'motif trouvé', 'contexte droit'])
        #Parcours de la list où le mot apparait afin de trouver le contexte avant et après
        for i in list:
            x = (self.get_doc(i).get_text().split(word))
            for j in range(0, len(x)-1):
                before = x[j]
                before = before.split()
                before.reverse()
                before = before[:int(lengthContext/2)]
                before.reverse()
                before = " ".join(before)
                after = x[j+1]
                after = after.split()[:int(lengthContext/2)]
                after = " ".join(after)
                listConcord = listConcord.append({'contexte gauche' : str(before), 'motif trouvé' : str(word), 'contexte droit' : str(after)}, ignore_index=(True))
        return listConcord
        
    
    #Création du vocabulaire avec les fréquences
    #Aide de https://www.geeksforgeeks.org/removing-stop-words-nltk-python/ pour la librairie nltk
    def vocabulaire(self):
        #Création de la liste du vocabulaire
        voca = []
        #Utilisation de NLTK pour enlever les mots vides 
        stopWords = stopwords.words('english')
        #Parcours du corpus
        for i in range (0, len(self.collection)):
            #Nettoyage du texte du document
            textClean = self.nettoyer_texte(self.collection[i].get_text())
            #On sépare les documents en mots
            wordsDocument = word_tokenize(textClean)
            #On parcours les mots afin d'ajouter les mots non vides au vocabulaire
            for w in wordsDocument:
                if w not in stopWords:
                    voca.append(w)
        #On transforme le dictionnaire en Series pandas
        voca = pandas.Series(voca)
        #On compte le nombre d'occurence d'un mot
        voca = voca.value_counts()
        return voca  
              
    #Création du vocabulaire enrichit du nombre de documents où apparaissent les mots du vocabulaire 
    def vocabulaireBest(self):
        #Recupération du vocabulaire et transformation en dataFrame
        voca = self.vocabulaire()
        voca = pandas.DataFrame({'word': voca.index, 'freq': voca.values})
        #Liste des nombres de documents
        listNbDocs = []
        #Parcours du vocabulaire afin de compter le nombre de document où le mot apparait
        for v in voca['word']:
            nbDocs = len(self.search(v))
            listNbDocs.append(nbDocs)
        #Ajout de la colonne de la liste du nombre de documents contenant les mots au vocabulaire
        voca['nbDocs'] = listNbDocs
        return voca
            
    
    #Nombre total de mots dans le corpus:
    def numberOfWords(self):
        #Variable de taille
        l = 0
        #Parcours du corpus
        for i in range (0, len(self.collection)):
            #Nettoyage du texte du document
            textClean = self.nettoyer_texte(self.collection[i].get_text())
            #Ajout du nombre de mots du document dans la taille totale
            l = l + len(textClean.split())
        return l
    
    #Mesure TFxIDF
    #Aide de https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76  pour
    #la compréhension de la mesure TFxIDF
    def TFxIDF(self):
        #Chargement du vocabulaire
        voca = self.vocabulaireBest()
        #Nombre de mots du corpus
        nbWords = self.numberOfWords()
        #Liste de mesure TFxIDF
        listTFxIDF = []
        #Parcours du vocabulaire
        for i in range (0, len(voca)):
            TF = (voca.iloc[i]['freq'])/(nbWords)
            IDF = math.log((self.ndoc)/(voca.iloc[i]['nbDocs']))
            if (IDF == 0):
                res = TF * 1
            else:
                res = TF * IDF
            listTFxIDF.append(res)
        #Ajout de la colonne TFxIDF au vocabulaire
        voca['TFxIDF'] = listTFxIDF
        return voca
        
    #Fonction retournant les n mots important du corpus suivant la mesure TFxIDF
    def bestWords(self, n):
        #Vérifie que n est bien un entier
        if (isinstance(n, int)):
        #Chargement du vocabulaire suivant la mesure TFxIDF
            voca = self.TFxIDF()
            #Tri suivant la colonne TFxIDF
            voca = voca.sort_values(by = ['TFxIDF'], ascending = False)
            return voca.head(n)
        else:
            print("Veuillez entrer un nombre valide !")
    
    #Fonction evolution d'un mot sur une courbe
    def Evolution_mot(self, w):
        all_docs = self.search(w) #Contient les numéros des docs qui contiennent le mot clé
    
        if len(all_docs) != 0: #Teste si le mot a été trouvé dans le corpus, si oui exécution du code ci-dessous
            #Initialisation des listes et dictionnaire qui vont contenir les données
            liste_date = []
            liste_occ = []
            dico_date = {}
        
            for i in all_docs: #parcours de tous les docs
                liste_date.append(self.get_doc(i).get_date()) #Liste contenant toutes les dates des documents qui contiennent le mot clé
                liste_occ.append(self.nettoyer_texte(self.get_doc(i).get_text()).count(self.nettoyer_texte(w))) #Liste contenant les occurences du mot clé dans les documents
            
            dico_date["Dates"] = liste_date #Ajout des dates dans le dictionnaire
            dico_date["Occurence"] = liste_occ #Ajout des occurences dans le dictionnaire
        
            df = pandas.DataFrame.from_dict(dico_date) #Création du DataFrame à partir du dictionnaire dico_date
            df.sort_values(by=['Dates'],inplace=True,ascending=True) #Trier le dataframe par date
            df['Occurence']=numpy.cumsum(df['Occurence']) #Transfomer les occurences en somme cumulée
            return df
        else: #Si le mot n'a pas été trouvé dans le corpus, affichage du message ci-dessous
            print("Le mot sélectionné n'apparait pas dans le corpus !")
        