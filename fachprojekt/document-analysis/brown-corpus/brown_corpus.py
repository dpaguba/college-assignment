import nltk
from nltk.corpus import brown
import matplotlib.pyplot as plt

# Laden Sie das Brown Corpus
nltk.download('brown')

'''
Hier werden die Kategorien des Brown Corpus abgerufen und in der Variable categories gespeichert.
'''
categories = brown.categories()

'''
In dieser Zeile wird eine Liste erstellt, die die Anzahl der Dokumente in jeder Kategorie enthält. 
Die Methode brown.fields(category) gibt die IDs der Dateien in der angegebenen Kategorie zurück, 
und len() gibt die Anzahl dieser IDs zurück.
'''
num_docs_per_category = [len(brown.fileids(category)) for category in categories]

'''
Hier wird eine Liste erstellt, die die Anzahl der Wörter in jeder 
Kategorie enthält. Die Methode brown.words(categories=category) gibt die Wörter in der angegebenen 
Kategorie zurück, und len() gibt die Anzahl dieser Wörter zurück.
'''
num_words_per_category = [len(brown.words(categories=category)) for category in categories]


