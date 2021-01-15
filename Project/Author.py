#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 08:12:01 2020

@author: quentinthomasson
"""

# Classe Auteur
class Author():
    # Constructeur
    def __init__(self, name):
        self.name = name
        self.production = {}
        self.ndoc = 0

    # Ajout d'un document à l'auteur
    def add(self, doc):
        self.production[self.ndoc] = doc
        self.ndoc += 1

    # Affichage
    def __str__(self):
        return "Auteur: " + self.name + ", Number of docs: " + str(self.ndoc)

    # Représentation
    def __repr__(self):
        return self.name
