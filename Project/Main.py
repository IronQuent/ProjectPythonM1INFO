#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 19:51:48 2021

@author: quentinthomasson
"""

################################## Import de librairies et classes ##################################

import praw

import urllib.request
import xmltodict

import datetime as dt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

import Document
import Corpus

################################## Création des Corpus ##################################

#Chargement des posts Reddit et ajout au corpus
def loadReddit(corpus_Reddit):
    reddit = praw.Reddit(client_id='NaUJwmnlGn4__g',
                         client_secret='nde8wjWh1Mn7OO2XpUx0Evbyz7I', user_agent='Reddit WebScraping')
    hot_posts = reddit.subreddit('Coronavirus').hot(limit=100)

    for post in hot_posts:
        datet = dt.datetime.fromtimestamp(post.created)
        txt = post.title + ". " + post.selftext
        txt = txt.replace('\n', ' ')
        txt = txt.replace('\r', ' ')
        doc = Document.RedditDocument(datet,
                                      post.title,
                                      post.author_fullname,
                                      txt,
                                      post.url,
                                      post.num_comments)
        corpus_Reddit.add_doc(doc)

#Chargement des posts Arxiv et ajout au corpus
def loadArxiv(corpus_Arxiv):
    url = 'http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=100'
    data = urllib.request.urlopen(url).read().decode()
    docs = xmltodict.parse(data)['feed']['entry']

    for i in docs:
        datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
        try:
            author = [aut['name'] for aut in i['author']][0]
        except:
            author = i['author']['name']
        txt = i['title'] + ". " + i['summary']
        txt = txt.replace('\n', ' ')
        txt = txt.replace('\r', ' ')
        try:
            coAuth = [aut['name'] for aut in i['author']][1:]
        except:
            coAuth = "Pas de Co-Auteur"
        doc = Document.ArxivDocument(datet,
                                     i['title'],
                                     author,
                                     txt,
                                     i['id'],
                                     coAuth
                                     )
        corpus_Arxiv.add_doc(doc)


#Initialisation des corpus
corpus_Reddit = Corpus.Corpus("Corona_red")
corpus_Arxiv = Corpus.Corpus("Corona_arx")

#Chargement des données dans les corpus
loadArxiv(corpus_Arxiv)
loadReddit(corpus_Reddit)

#Affichage du nombre de documents et d'auteurs
print("Création du corpus Reddit, %d documents et %d auteurs" %
      (corpus_Reddit.ndoc, corpus_Reddit.naut))
print("Création du corpus Arxiv, %d documents et %d auteurs" %
      (corpus_Arxiv.ndoc, corpus_Arxiv.naut))

print()

#Enregistrement des corpus
print("Enregistrement des corpus sur le disque...")
corpus_Reddit.save("Corona_red.crp")
corpus_Arxiv.save("Corona_arx.crp")

#Afficher le dataframe des mots les plus importants
def affichageDF(self, n, textDFReddit, textDFArxiv):
    try:
        #Création splash de l'analyse
        splash = SplashAnalyse(self)
        #Cast de n
        n = int(n)
        #Champ d'affichage du dataframe Reddit
        textDFReddit.delete(1.0, tk.END)
        textDFReddit.insert(tk.END, "Corpus REDDIT\n\n", 'normal')
        textDFReddit.insert(tk.END, str(corpus_Reddit.bestWords(n)))
        textDFReddit.pack()
        #Champ d'affichage du dataframe Arxiv
        textDFArxiv.delete(1.0, tk.END)
        textDFArxiv.insert(tk.END, "Corpus ARXIV\n\n", 'normal')
        textDFArxiv.insert(tk.END, str(corpus_Arxiv.bestWords(n)))
        textDFArxiv.pack()
        #Destruction du splash
        splash.destroy()
    except ValueError as error:
        splash.destroy()
        splash = SplashErrorNumber(self)

#Afficher la courbe du mot passé en paramètre
def affichageCourbe(self, word, f, canvas):
    try:
        #Récupération des dataframe de l'évolution d'un mot dans le temps
        DFArxiv = corpus_Arxiv.Evolution_mot(word)
        DFReddit = corpus_Reddit.Evolution_mot(word)
        #Si les dataframes ne sont pas vides
        if (DFArxiv is None and DFReddit is None):
            splash = SplashErrorWord(self)
        else:
            #Nettoie la courbe
            f.clear()
            a = f.add_subplot(111)
            #Ajout des dataframes au graphique
            if (DFArxiv is not None):
                a.plot(DFArxiv['Dates'], DFArxiv['Occurence'], label="Arxiv")
            if (DFReddit is not None):
                a.plot(DFReddit['Dates'],
                       DFReddit['Occurence'], label="Reddit")
            #Attribution des titres
            a.set_title("Analyse pour " + str(word))
            a.set_xlabel("Date")
            a.set_ylabel("Nombre d'apparitions")
            #Ajout
            a.legend()
            canvas.draw()
    #En cas d'erreur
    except TypeError as error:
        splash = SplashErrorWord(self)

################################## Création de l'interface graphique ##################################


#Police et taille
LARGE_FONT = ("Arial", 20)

#Classe principale
#Aide de https://pythonprogramming.net/change-show-new-frame-tkinter/ pour la mise en place
class InterfaceGraphique(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title("Analyse comparative de corpus")
        self.geometry("1000x800")

        self.frames = {}

        for F in (PageMenu, PageSearch, PageWords):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageMenu)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


#Page comparaison mots
class PageWords(tk.Frame):

    def __init__(self, parent, controller):
        #Init
        tk.Frame.__init__(self, parent)

        #Label du titre dans la fenêtre
        titreMethode = tk.Label(
            self, text="Comparaison de mots issus des corpus", font=LARGE_FONT)
        titreMethode.pack(pady=5)

        #Label de la description du champ de saisie
        titreLabel = tk.Label(
            self, text="Entrez le nombre de mots les plus fréquents à afficher : ", font=('Arial', 14))
        titreLabel.pack(pady=5)

        #Champ de saisie
        champNbWord = tk.StringVar()
        entryNbWord = tk.Entry(self, textvariable=champNbWord, width=10)
        entryNbWord.pack(pady=5)

        #Champ texte affichage DF
        textDFReddit = tk.Text(self, height=20, width=60)
        textDFArxiv = tk.Text(self, height=20, width=60)
        textDFArxiv.tag_configure(
            'normal', font=('Arial', 14), justify='center')
        textDFReddit.tag_configure(
            'normal', font=('Arial', 14), justify='center')

        #Boutons
        boutonValidation = tk.Button(self, text="Analyser", relief=tk.GROOVE, command=lambda: affichageDF(
            self, champNbWord.get(), textDFReddit, textDFArxiv))
        boutonValidation.pack(pady=5)

        #Bouton retour au menu
        buttonMenu = tk.Button(self, text="MENU", relief=tk.GROOVE,
                               command=lambda: controller.show_frame(PageMenu))
        buttonMenu.pack(pady=5)

#Page menu
class PageMenu(tk.Frame):

    def __init__(self, parent, controller):
        #Init
        tk.Frame.__init__(self, parent)

        #Label du titre dans la fenêtre
        titreMenu = tk.Label(self, text="MENU", font=LARGE_FONT)
        titreMenu.pack(pady=10, padx=10)

        #Boutons
        buttonM1 = tk.Button(self, text="Comparaison de mots des corpus",
                             relief=tk.GROOVE, command=lambda: controller.show_frame(PageWords))
        buttonM1.pack(pady=5)

        buttonM2 = tk.Button(self, text="Recherche de mots dans les corpus",
                             relief=tk.GROOVE, command=lambda: controller.show_frame(PageSearch))
        buttonM2.pack(pady=5)

#Page Recherche
class PageSearch(tk.Frame):

    def __init__(self, parent, controller):
        #Init
        tk.Frame.__init__(self, parent)

        #Label du titre dans la fenêtre
        titreMenu = tk.Label(
            self, text="Recherche de mots dans les corpus", font=LARGE_FONT)
        titreMenu.pack(pady=10, padx=10)

        #Label de la description du champ de saisie
        titreLabel = tk.Label(
            self, text="Entrez le mot a rechercher : ", font=('Arial', 14))
        titreLabel.pack(pady=5)

        #Champ de saisie
        champWord = tk.StringVar()
        entryWord = tk.Entry(self, textvariable=champWord, width=10)
        entryWord.pack(pady=5)

        #Boutons
        boutonValidation = tk.Button(self, text="Rechercher", relief=tk.GROOVE,
                                     command=lambda: affichageCourbe(self, champWord.get(), f, canvas))
        boutonValidation.pack(pady=5)

        #Bouton retour au menu
        buttonMenu = tk.Button(self, text="MENU", relief=tk.GROOVE,
                               command=lambda: controller.show_frame(PageMenu))
        buttonMenu.pack(pady=5)

        #Figure contenant la courbe
        f = Figure(figsize=(20, 15), dpi=100)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


#Fenêtre affichant une erreur de mot recherché
class SplashErrorWord(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        #Label du titre dans la fenêtre
        txt = tk.Label(self, text="Mot inexistant !", font=LARGE_FONT)
        txt.pack(pady=10, padx=10)

        #Boutons
        button = tk.Button(self, text="OK", relief=tk.GROOVE,
                           command=self.destroy)
        button.pack(pady=5)

        self.update()

#Fenêtre affichant une erreur de mot recherché
class SplashErrorNumber(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        #Label du titre dans la fenêtre
        txt = tk.Label(
            self, text="Veuillez entrer un nombre valide !", font=LARGE_FONT)
        txt.pack(pady=10, padx=10)

        #Boutons
        button = tk.Button(self, text="OK", relief=tk.GROOVE,
                           command=self.destroy)
        button.pack(pady=5)

        self.update()

#Fenêtre affichant le chargement de l'analyse
class SplashAnalyse(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        #Label du titre dans la fenêtre
        txt = tk.Label(self, text="Analyse en cours...", font=LARGE_FONT)
        txt.pack(pady=10, padx=10)

        self.update()


################################## Main ##################################

#Main
app = InterfaceGraphique()
app.mainloop()
