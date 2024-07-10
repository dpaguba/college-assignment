import matplotlib.pyplot as plt
import numpy as np

class RandomArrayGenerator(object):
    
    def __init__(self, seed=None):
        """ Initialisiert den Zufallsgenerator
        Params:
            seed: Zufallssaat
        """
        if seed is not None:
            np.random.seed(seed)
    
    def rand_uniform(self, arr_shape, min_elem=0, max_elem=1):
        """ Generiert eine Liste mit gleichverteilten Zufallszahlen
        Params:
            n_elem: Anzahl von Elementen in der Liste
            min_elem: Kleinstmoegliches Element 
            max_elem: Groesstmoegliches Element
        Returns: NumPy Array mit Zufallszahlen            
        """
        rand_arr = np.random.rand(*arr_shape)
        rand_arr = min_elem + rand_arr * (max_elem - min_elem)
        return rand_arr
            
    def rand_gauss(self, arr_shape, mean=0, std_deviation=1):
        """ Generiert eine Liste mit normalverteilten Zufallszahlen
        Params:
            n_elem: Anzahl von Elementen in der Liste
            min_elem: Kleinstmoegliches Element 
            max_elem: Groesstmoegliches Element
        Returns: NumPy Array mit Zufallszahlen
            
        """
        # Der * Operator expandiert ein tuple Objekt in eine Parameter Liste
        # https://docs.python.org/2/tutorial/controlflow.html#unpacking-argument-lists
        rand_arr = np.random.randn(*arr_shape)
        rand_arr = mean + rand_arr * std_deviation
        return rand_arr

def bar_plot(ax, x_values, y_values, y_err=None, title=None):
    """ Plottet ein vertikales Balkendiagramm
    Params:
        ax: Axes-Objekt, in das geplottet werden soll.
        x_values: Liste von x Werten. Auf None setzen, um den Index aus y_values
            zu verwenden. (Automatische Anzahl / Platzierung der x-ticks).
        y_values: Liste von y Werten
        y_err: Abweichungen fuer Fehlerbalken
        title: Ueberschrift des Plots
    """
    x_pos = np.arange(len(y_values))
    ax.bar(x_pos, y_values, width=0.9, align='center', alpha=0.4, yerr=y_err)
    if x_values is not None:
        ax.set_xticks(np.linspace(0, len(y_values), len(x_values)))  # , x_values, rotation='vertical')
    if title is not None:
        ax.set_title(title)