import string
import numpy as np
from collections import defaultdict
from common.corpus import CorpusLoader
from nltk.stem.porter import PorterStemmer  # IGNORE:import-error
import cv2
from collections import Counter
from math import log





class AbsoluteTermFrequencies(object):
    """Klasse, die zur Durchfuehrung absoluter Gewichtung von Bag-of-Words
    Matrizen (Arrays) verwendet werden kann. Da Bag-of-Words zunaechst immer in
    absoluten Frequenzen gegeben sein muessen, ist die Implementierung dieser 
    Klasse trivial. Sie wird fuer die softwaretechnisch eleganten Unterstuetzung
    verschiedner Gewichtungsschemata benoetigt (-> Duck-Typing).   
    """

    @staticmethod
    def weighting(bow_mat):
        """Fuehrt die Gewichtung einer Bag-of-Words Matrix durch.
        
        Params:
            bow_mat: Numpy ndarray (d x t) mit Bag-of-Words Frequenzen je Dokument
                (zeilenweise).
                
        Returns:
            bow_mat: Numpy ndarray (d x t) mit *gewichteten* Bag-of-Words Frequenzen 
                je Dokument (zeilenweise).
        """
        # Gibt das NumPy Array unveraendert zurueck, da die Bag-of-Words Frequenzen
        # bereits absolut sind.
        #return bow_mat

    def __repr__(self):
        """Ueberschreibt interne Funktion der Klasse object. Die Funktion wird
        zur Generierung einer String-Repraesentations des Objekts verwendet.
        Sie wird durch den Python Interpreter bei einem Typecast des Objekts zum
        Typ str ausgefuehrt. Siehe auch str-Funktion.
        """
        return 'absolute'

    def __format__(self, format_spec):
        """Ueberschreibt interne Funktion der Klasse object. Die Funktion wird
        zur Generierung einer String-Repraesentation des Objekts verwendet.
        Sie wird durch den Python Interpreter ausgefuehrt, wenn das Objekt einer
        'format' methode uebergeben wird."""
        return format(str(self), format_spec)


class RelativeTermFrequencies(object):
    """Realisiert eine Transformation von in absoluten Frequenzen gegebenen 
    Bag-of-Words Matrizen (Arrays) in relative Frequenzen.
    """

    @staticmethod
    def weighting(bow_mat):
        """Fuehrt die relative Gewichtung einer Bag-of-Words Matrix (relativ im 
        Bezug auf Dokumente) durch.
        
        Params:
            bow_mat: Numpy ndarray (d x t) mit Bag-of-Words Frequenzen je Dokument
                (zeilenweise).
                
        Returns:
            bow_mat: Numpy ndarray (d x t) mit *gewichteten* Bag-of-Words Frequenzen 
                je Dokument (zeilenweise).
        """
        
        # Berechnung der Summe jeder Zeile (Summe der absoluten Häufigkeiten)
        row_sums = bow_mat.sum(axis=1)
        # Division jeder Zeile durch ihre Summe, um relative Häufigkeiten zu erhalten
        bow_mat = bow_mat / row_sums[:, np.newaxis]
        return bow_mat
        
        

    def __repr__(self):
        """Ueberschreibt interne Funktion der Klasse object. Die Funktion wird
        zur Generierung einer String-Repraesentations des Objekts verwendet.
        Sie wird durch den Python Interpreter bei einem Typecast des Objekts zum
        Typ str ausgefuehrt. Siehe auch str-Funktion.
        """
        return 'relative'

    def __format__(self, format_spec):
        """Ueberschreibt interne Funktion der Klasse object. Die Funktion wird
        zur Generierung einer String-Repraesentation des Objekts verwendet.
        Sie wird durch den Python Interpreter ausgefuehrt, wenn das Objekt einer
        'format' methode uebergeben wird."""
        return format(str(self), format_spec)


class RelativeInverseDocumentWordFrequecies(object):
    """Realisiert eine Transformation von in absoluten Frequenzen gegebenen 
    Bag-of-Words Matrizen (Arrays) in relative - inverse Dokument Frequenzen.
    """

    def __init__(self, vocabulary, category_wordlists_dict):
        """Initialisiert die Gewichtungsberechnung, indem die inversen Dokument
        Frequenzen aus dem Dokument Korpous bestimmt werden.
        
        Params:
            vocabulary: Python Liste von Woertern (das Vokabular fuer die 
                Bag-of-Words).
            category_wordlists_dict: Python dictionary, das zu jeder Klasse (category)
                eine Liste von Listen mit Woertern je Dokument enthaelt.
                Siehe Beschreibung des Parameters cat_word_dict in der Methode
                BagOfWords.category_bow_dict.
        """
        #raise NotImplementedError()
        self.vocabulary = vocabulary
        self.category_wordlists_dict = category_wordlists_dict
        self.term_document_counts = self.calculate_term_document_counts()
        self.idf_values = self.calculate_idf_values()
        
    def calculate_term_document_counts(self):
        term_document_counts = defaultdict(int)
        for category, wordlists in self.category_wordlists_dict.items():
            for wordlist in wordlists:
                unique_words = set(wordlist)
                for word in unique_words:
                    term_document_counts[word] += 1
        return term_document_counts

    def calculate_idf_values(self):
        total_documents = sum(len(wordlists) for wordlists in self.category_wordlists_dict.values())
        idf_values = {}
        for term, document_count in self.term_document_counts.items():
            idf_values[term] = np.log(total_documents / document_count)
        return idf_values

    def plot_idf_values(self):
        sorted_terms = sorted(self.idf_values.items(), key=lambda x: x[1], reverse=True)
        terms, idfs = zip(*sorted_terms)
        plt.figure(figsize=(10, 6))
        plt.barh(terms[:30], idfs[:30])
        plt.xlabel('IDF Value')
        plt.ylabel('Term')
        plt.title('Inverse Document Frequency (IDF) for Terms in Brown Corpus')
        plt.gca().invert_yaxis()
        plt.show()

    def weighting(self, bow_mat):
        """Fuehrt die Gewichtung einer Bag-of-Words Matrix durch.
        
        Params:
            bow_mat: Numpy ndarray (d x t) mit Bag-of-Words Frequenzen je Dokument
                (zeilenweise).
                
        Returns:
            bow_mat: Numpy ndarray (d x t) mit *gewichteten* Bag-of-Words Frequenzen 
                je Dokument (zeilenweise).
        """
        #raise NotImplementedError()
        return bow_mat

    def __repr__(self):
        """Ueberschreibt interne Funktion der Klasse object. Die Funktion wird
        zur Generierung einer String-Repraesentations des Objekts verwendet.
        Sie wird durch den Python Interpreter bei einem Typecast des Objekts zum
        Typ str ausgefuehrt. Siehe auch str-Funktion.
        """
        return 'tf-idf'

    def __format__(self, format_spec):
        """Ueberschreibt interne Funktion der Klasse object. Die Funktion wird
        zur Generierung einer String-Repraesentation des Objekts verwendet.
        Sie wird durch den Python Interpreter ausgefuehrt, wenn das Objekt einer
        'format' methode uebergeben wird."""
        return format(str(self), format_spec)


class BagOfWords(object):
    """Berechnung von Bag-of-Words Repraesentationen aus Wortlisten bei 
    gegebenem Vokabular.
    """

    def __init__(self, vocabulary, term_weighting=AbsoluteTermFrequencies()):
        """Initialisiert die Bag-of-Words Berechnung
        
        Params:
            vocabulary: Python Liste von Woertern / Termen (das Bag-of-Words Vokabular).
                Die Reihenfolge der Woerter / Terme im Vokabular gibt die Reihenfolge
                der Terme in den Bag-of-Words Repraesentationen vor.
            term_weighting: Objekt, das die weighting(bow_mat) Methode implemeniert.
                Optional, verwendet absolute Gewichtung als Default.
        """
        self.__vocabulary = vocabulary
        self.__term_weighting = term_weighting
        
        
    def category_bow_dict(self, cat_word_dict):
        """Erzeugt ein dictionary, welches fuer jede Klasse (category)
        ein NumPy Array mit Bag-of-Words Repraesentationen enthaelt.
        
        Params:
            cat_word_dict: Dictionary, welches fuer jede Klasse (category)
                eine Liste (Dokumente) von Listen (Woerter) enthaelt.
                cat : [ [word1, word2, ...],  <--  doc1
                        [word1, word2, ...],  <--  doc2
                        ...                         ...
                        ]
        Returns:
            category_bow_mat: Ein dictionary mit Bag-of-Words Matrizen fuer jede
                Kategory. Eine Matrix enthaelt in jeder Zeile die Bag-of-Words 
                Repraesentation eines Dokuments der Kategorie. (d x t) bei d 
                Dokumenten und einer Vokabulargroesse t (Anzahl Terme). Die
                Reihenfolge der Terme ist durch die Reihenfolge der Worter / Terme
                im Vokabular (siehe __init__) vorgegeben.
        """
       #teil2
        category_bow_dict = {}
        for category, word_lists in cat_word_dict.items():
            bow_matrix = np.zeros((len(word_lists), len(self.__vocabulary)), dtype=int)
            for i, word_list in enumerate(word_lists):
                word_counter = Counter(word_list)
                for j, word in enumerate(self.__vocabulary):
                    bow_matrix[i, j] = word_counter[word]
            category_bow_dict[category] = bow_matrix
        return category_bow_dict 

    
    @staticmethod
    def most_freq_words(word_list, n_words=None):
        """Bestimmt die (n-)haeufigsten Woerter in einer Liste von Woertern.
        
        Params:
            word_list: Liste von Woertern
            n_words: (Optional) Anzahl von haeufigsten Woertern (top n). Falls
                n_words mit None belegt ist, sollen alle vorkommenden Woerter
                betrachtet werden.
            
        Returns:
            words_topn: Python Liste, die (top-n) am haeufigsten vorkommenden 
                Woerter enthaelt. Die Sortierung der Liste ist nach Haeufigkeit
                absteigend.
        """
          # Zähle die Häufigkeit der Wörter
        word_counter = Counter(word_list)

        # Falls n_words nicht angegeben ist, betrachte alle Wörter
        if n_words is None:
            words_topn = word_counter.most_common()
        else:
            words_topn = word_counter.most_common(n_words)

        return [word for word, count in words_topn]
    


class WordListNormalizer(object):

    def __init__(self, stoplist=None, stemmer=None):
        """Initialisiert die Filter
        
        Params: 
            stoplist: Python Liste von Woertern, die entfernt werden sollen
                (stopwords). Optional, verwendet NLTK stopwords falls None
            stemmer: Objekt, das die stem(word) Funktion implementiert. Optional,
                verwendet den Porter Stemmer falls None.
        """

        if stoplist is None:
            stoplist = CorpusLoader.stopwords_corpus()
        self.__stoplist = stoplist

        if stemmer is None:
            stemmer = PorterStemmer()
        self.__stemmer = stemmer
        self.__punctuation = string.punctuation
        self.__delimiters = ["''", '``', '--']

    
    def normalize_words(self, word_list):
        """Normalisiert die gegebenen Woerter nach in der Methode angwendeten
        Filter-Regeln (Gross-/Kleinschreibung, stopwords, Satzzeichen, 
        Bindestriche und Anfuehrungszeichen, Stemming)
        
        Params: 
            word_list: Python Liste von Worten.
            
        Returns:
            word_list_filtered, word_list_stemmed: Tuple von Listen
                Bei der ersten Liste wurden alle Filterregeln, bis auch stemming
                angewandt. Bei der zweiten Liste wurde zusaetzlich auch stemming
                angewandt.
        """
         # Groß- und Kleinschreibung normalisieren
        word_list_lower = [word.lower() for word in word_list]

        # Entfernen von Satzzeichen und Delimiters
        word_list_filtered = [word for word in word_list_lower if word not in self.__punctuation and word not in self.__delimiters]

        # Entfernen von stopwords
        word_list_filtered = [word for word in word_list_filtered if word not in self.__stoplist]

        # Stemming
        word_list_stemmed = [self.__stemmer.stem(word) for word in word_list_filtered]

        return word_list_filtered, word_list_stemmed
      
        
    #teil
    def category_wordlists_dict(self, corpus):
        """Wir transformieren a corpus to a dictionary mit Liste von Listen
        
        Params:
            corpus: NLTK corpus object.
        
        Returns:
            category_wordlists_dict: Dictionary wo die Keys sind Kategorien und Values sind Liste von Listen.
                Liste Draußen ist für Dokumenten Pro Kategorie
                Liste Innen die Normalized words für jeder Dokument
        """
        category_wordlists_dict = {}
        categories = corpus.categories()
        for category in categories:
            documents = corpus.fileids(categories=category)
            category_wordlists_dict[category] = []
            for document in documents:
                words = corpus.words(fileids=document)
                #documents = corpus.fileids(categories=category,fileids=document)
                normalized_words = self.normalize_words(words)[1]
                category_wordlists_dict[category].append(normalized_words)
        return category_wordlists_dict

    


class IdentityFeatureTransform(object):
    """Realisert eine Transformation auf die Identitaet, bei der alle Daten 
    auf sich selbst abgebildet werden. Die Klasse ist hilfreich fuer eine
    softwaretechnisch elegante Realisierung der Funktionalitaet "keine Transformation
    der Daten durchfuehren" (--> Duck-Typing).
    """

    def estimate(self, train_data, train_labels):
        pass

    def transform(self, data):
        return data


class TopicFeatureTransform(object):
    """Realsiert statistische Schaetzung eines Topic Raums und Transformation
    in diesen Topic Raum.
    """

    def __init__(self, topic_dim):
        """Initialisiert die Berechnung des Topic Raums
        
        Params:
            topic_dim: Groesse des Topic Raums, d.h. Anzahl der Dimensionen.
        """
        self.__topic_dim = topic_dim
        # Transformation muss in der estimate Methode definiert werden.
        self.__T = None
        self.__S_inv = None

    def estimate(self, train_data, train_labels):  # IGNORE:unused-argument
        """Statistische Schaetzung des Topic Raums
        
        Params:
            train_data: ndarray, das Merkmalsvektoren zeilenweise enthaelt (d x t).
            train_labels: ndarray, das Klassenlabels spaltenweise enthaelt (d x 1).
                Hinweis: Fuer den hier zu implementierenden Topic Raum werden die
                Klassenlabels nicht benoetigt. Sind sind Teil der Methodensignatur
                im Sinne einer konsitenten und vollstaendigen Verwaltung der zur
                Verfuegung stehenden Information.
            
            mit d Trainingsbeispielen und t dimensionalen Merkmalsvektoren.
        """
        raise NotImplementedError()


    def transform(self, data):
        """Transformiert Daten in den Topic Raum.
        
        Params:
            data: ndarray, das Merkmalsvektoren zeilenweise enthaelt (d x t).
        
        Returns:
            data_trans: ndarray der in den Topic Raum transformierten Daten 
                (d x topic_dim).
        """
        raise NotImplementedError()


def compute_sift_descriptors(im_arr, cell_size=5, step_size=20):
    """
    Berechnet SIFT Deskriptoren in einem regulären Gitter

    Params:
        im_array: ndarray, mit dem Eingabebild in Graustufen (n x n x 1)
        cell_size: int, Größe einer Zelle des SIFT Deskriptors in Pixeln
        step_size: int, Schrittweite im regulären Gitter in Pixeln

    Returns:
        frames: list, mit x,y Koordinaten der Deskriptor Mittelpunkte
        desc: ndarray, mit den berechneten SIFT Deskriptoren (N x 128)

    """
    # Generate dense grid
    frames = [(x, y) for x in np.arange(10, im_arr.shape[1], step_size, dtype=np.float32)
              for y in np.arange(10, im_arr.shape[0], step_size, dtype=np.float32)]

    # Note: In the standard SIFT detector algorithm, the size of the
    # descriptor cell size is related to the keypoint scal by the magnification factor.
    # Therefore the size of the is equal to cell_size/magnification_factor (Default: 3)
    kp = [cv2.KeyPoint(x, y, cell_size / 3) for x, y in frames]

    sift = cv2.SIFT_create()

    sift_features = sift.compute(im_arr, kp)
    desc = sift_features[1]
    return frames, desc
