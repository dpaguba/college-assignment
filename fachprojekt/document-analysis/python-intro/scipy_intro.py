import numpy as np
import sys

if '..' not in sys.path:
    sys.path.append('..')

from common.python_intro_functions import RandomArrayGenerator, bar_plot

rand_list = [1, 3, 5, 2, 7, 4, 9, 0, 6]
rand_arr = np.array(rand_list)
print(type(rand_arr))

zeros_arr = np.zeros((3, 3))
print(zeros_arr)

seq_arr = np.arange(100).reshape(10, 10)
print(seq_arr.shape)
print(seq_arr)

# Zugriffsfunktionen und Slicing
print(seq_arr[:3, :2])  # obere (3, 2) Matrix
print(seq_arr[-3:, -3:])  # untere (3, 3) Matrix
print(seq_arr[3, :])  # 4. Zeile
print(seq_arr[:, ::2])  # jede ungerade Spalte
print(seq_arr[:, [2, 3, 6, 7]])  # Spalten mit Index 2, 3, 6, 7

# Boolean Indexing
seq_arr[seq_arr % 2 == 1] = 0
print(seq_arr)

# Mathematische Operation
print(seq_arr[0, :] + seq_arr[1, :])  # elementweise Summe der ersten beiden Zeilen
print(seq_arr[0, :] * seq_arr[1, :])  # elementweise Produkt der ersten beiden Zeilen
print(np.dot(seq_arr[0, :], seq_arr[1, :]))  # Skalarprodukt der ersten beiden Zeilen

x = np.arange(5)
w = np.asarray([1.0, 2.0, 1.5, 0.5, 4.2])
print(np.dot(x, w))  # gewichtete Summe

X = np.arange(20).reshape((4, 5))
print(np.dot(X, w))  # gewichtete Summen für mehrere Eingaben

W = np.asarray([[1.0, 2.0, 1.5, 0.5, 4.2],
                [0.5, 3.0, 1.2, 1.3, 0.2],
                [3.5, 4.3, 2.7, 3.1, 0.2]])
print(np.dot(X, W.T))  # gewichtete Summen für mehrere Eingaben und Gewichtungen

# Wichtige Funktionen
print(np.max(seq_arr, axis=1))  # größtes Element in jeder Zeile
print(np.argmax(seq_arr, axis=1))  # Index des größten Elements in jeder Zeile
print(np.sum(seq_arr, axis=1))  # Summe entlang jeder Zeile
print(np.mean(seq_arr, axis=1))  # Mittelwert entlang jeder Zeile


# ---------------------------------------------------------------------

# Runden Sie die Elemente der Arrays (ganzzahlig)
rand_arr_gauss_rounded = np.around(rand_arr_gauss)
rand_arr_unif_rounded = np.around(rand_arr_unif)

# Erstellen Sie Histogramme
hist_gauss = np.bincount(rand_arr_gauss_rounded.astype(int))
hist_unif = np.bincount(rand_arr_unif_rounded.reshape(-1).astype(int))

# Plotten Sie die Ergebnisse
fig, axs = plt.subplots(2)

axs[0].bar(range(len(hist_gauss)), hist_gauss)
axs[0].set_title('Histogram of rand_arr_gauss')

axs[1].bar(range(len(hist_unif)), hist_unif)
axs[1].set_title('Histogram of rand_arr_unif')

plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------
# Modified 2025-08-11 10:24:30