import numpy as np
import scipy.spatial.distance
from common.features import BagOfWords, IdentityFeatureTransform



class KNNClassifier(object):

    def __init__(self, k_neighbors, metric):
        """Initialisiert den Klassifikator mit Meta-Parametern
        
        Params:
            k_neighbors: Anzahl der zu betrachtenden naechsten Nachbarn (int)
            metric: Zu verwendendes Distanzmass (string), siehe auch scipy Funktion cdist 
        """
        self.__k_neighbors = k_neighbors
        self.__metric = metric
        # Initialisierung der Membervariablen fuer Trainingsdaten als None. 
        self.__train_bow = None
        self.__train_labels = None

    def estimate(self, train_bow, train_labels):
        """Erstellt den k-Naechste-Nachbarn Klassfikator mittels Trainingdaten.
        
        Der Begriff des Trainings ist beim K-NN etwas irre fuehrend, da ja keine
        Modelparameter im eigentlichen Sinne statistisch geschaetzt werden. 
        Diskutieren Sie, was den K-NN stattdessen definiert.
        
        Hinweis: Die Funktion heisst estimate im Sinne von durchgaengigen Interfaces
                fuer das Duck-Typing
        
        Params:
            train_samples: ndarray, das Merkmalsvektoren zeilenweise enthaelt (d x t).
            train_labels: ndarray, das Klassenlabels spaltenweise enthaelt (d x 1).
            
            mit d Trainingsbeispielen und t dimensionalen Merkmalsvektoren.
        """
        self.__train_bow = train_bow
        self.__train_labels = train_labels
       
    def classify(self, test_bow):
        """Klassifiziert Test Daten.
        
        Params:
            test_samples: ndarray, das Merkmalsvektoren zeilenweise enthaelt (d x t).
            
        Returns:
            test_labels: ndarray, das Klassenlabels spaltenweise enthaelt (d x 1).
        
            mit d Testbeispielen und t dimensionalen Merkmalsvektoren.
        """
        
        if self.__train_bow is None or self.__train_labels is None:
            raise ValueError('Classifier has not been "estimated", yet!')
        train_bow =self.__train_bow
        train_labels = self.__train_labels
        
        k = self.__k_neighbors
        metrik = self.__metric
        dis = scipy.spatial.distance.cdist(test_bow, train_bow, metrik)
        sort = np.argsort(dis, axis = 1)[:,:k]
        copy_train_labels = train_labels.ravel()
       
        test_labels = copy_train_labels[sort]
       
        list_test_labels = test_labels.tolist()

        list_copy_train_labels = copy_train_labels.tolist()
        
        
        Bagof = BagOfWords(list_copy_train_labels)
        listreturn = []
        for i in list_test_labels:
            listreturn.append(Bagof.most_freq_words(i,1))
            
        
        return np.asarray(listreturn)
   