#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 08:14:10 2020

@author: quentinthomasson
"""
#Librairie
from gensim.summarization.summarizer import summarize

#Classe document
class Document():
    
    #Constructeur
    def __init__(self, date, title, author, text, url):
        self.date = date
        self.title = title
        self.author = author
        self.text = text
        self.url = url
    
    #Obtenir l'auteur
    def get_author(self):
        return self.author

    #Obtenir le titre
    def get_title(self):
        return self.title
    
    #Obtenir la date
    def get_date(self):
        return self.date
    
    #Obtenir l'url
    def get_source(self):
        return self.source
    
    #Obtenir le texte    
    def get_text(self):
        return self.text
    
    #Affichage
    def __str__(self):
        return "Document " + str(self.getType()) + " : " + self.title + "\nAuthor : " + self.author
    
    #Représentation
    def __repr__(self):
        return self.title
    
    #Résumer
    def sumup(self,ratio):
        try:
            auto_sum = summarize(self.text,ratio=ratio,split=True)
            out = " ".join(auto_sum)
        except:
            out =self.title            
        return out
    
    #Obtenir le type du document
    def getType(self):
        pass
    
    
#Classe Reddit héritant de document   
class RedditDocument(Document):  
    #Constructeur
    def __init__(self, date, title, author, text, url, nbCommentary = 0):
        super().__init__(date = date, title = title, author = author, text = text, url = url)
        self.nbCommentary = nbCommentary
        
    #Obtenir le nombre de commentaires
    def get_nbCommentary(self):
        return self.nbCommentary
    
    #Affichage
    def __str__(self):
        return Document.__str__(self) + "\nNb Commentary : " + str(self.nbCommentary)
    
    #Obtenir le type
    def getType(self):
        return "Reddit Document"

#Classe Arxiv héritant de document
class ArxivDocument(Document):
    #Constructeur
    def __init__(self, date, title, author, text, url, coAuthor = []):
        super().__init__(date = date, title = title, author = author, text = text, url = url)
        self.coAuthor = coAuthor

    #Obtenir les co-auteurs
    def get_coAuthor(self):
        return self.coAuthor
    
    #Affichage
    def __str__(self):
        #return Document.__str__(self) + "\nCo-Author : " + str(self.coAuthor)
        return Document.__str__(self) + "\nCo-Author : " + ", ".join(self.coAuthor)
    
    #Obtenir le type
    def getType(self):
        return "Arxiv Document"