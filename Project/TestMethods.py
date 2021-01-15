#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 10:05:59 2021

@author: quentinthomasson
"""

#Librairies
import unittest
import Corpus
import Document

#Classe réalisant les tests unitaires
#Aide de https://docs.python.org/3/library/unittest.html pour la mise en place
class TestMethods(unittest.TestCase):
    
    #Vérification du bon fonctionnement de la fonction de nettoyage
    def testNettoyage(self):
        testCorpus = Corpus.Corpus("testCorpus")
        textClean = testCorpus.nettoyer_texte("45Bonjour-321")
        self.assertEqual(textClean, "  bonjour    ")

    #Verification si le corpus est vide
    def testCorpusEmpty(self):
        testCorpus = Corpus.Corpus("testCorpus")
        self.assertEqual(testCorpus.get_coll(), {})
    
    #Verification du type de document 
    def testDocumentType(self):
        doc = Document.RedditDocument("2021-01-01", "test", "anonymous", "This is a test doc", "http://test.eu")
        self.assertEqual(doc.getType(), "Reddit Document")
    
#Main
if __name__ == '__main__':
    unittest.main()
