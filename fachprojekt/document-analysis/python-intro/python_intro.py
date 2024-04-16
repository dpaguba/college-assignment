import sys

if '..' not in sys.path:
    sys.path.append('..')
import numpy as np
from common.python_intro_functions import RandomArrayGenerator

# Einführung in Python

'''
Dieser Code überprüft, ob 42 oder 23 in dem Tuple variable 
vorhanden ist und gibt eine entsprechende Nachricht auf der Konsole aus.
'''

variable = (1, 1.0, '1.0')
print(type(variable))

if 42 in variable or 23 in variable:
    print("Either 42 or 23 is in the tuple.")
elif 42 not in variable and 23 not in variable:
    print("Neither 42 nor 23 is in the tuple.")
else:
    print("Only one of 42 or 23 is in the tuple.")

# ---------------------------------------------------------------------

'''
Um die Anzahl der Elemente in der Liste test_list zu bestimmen, 
kann man die eingebaute Python-Funktion len() verwenden.
'''

test_list = list(range(10, 33, 2))
print(test_list)

num_elements = len(test_list)
print("Number of elements in the list: ", num_elements)

# ---------------------------------------------------------------------

'''
Um die angeforderten Elemente und Teile der Liste test_list zu erhalten, 
kann man die Indexierung und Slicing-Funktionen von Python verwenden.
'''

# Das erste, letzte und vorletzte Element
first_element = test_list[0]
last_element = test_list[-1]
penultimate_element = test_list[-2]

print("First element: ", first_element)
print("Last element: ", last_element)
print("Penultimate element: ", penultimate_element)

# Das erste, zweite und letzte Drittel
third_length = len(test_list) // 3

first_third = test_list[:third_length]
second_third = test_list[third_length:2*third_length]
last_third = test_list[2*third_length:]

print("First third: ", first_third)
print("Second third: ", second_third)
print("Last third: ", last_third)

# ---------------------------------------------------------------------

'''
Um alle Elemente der for-Schleide durchzulaufen, kann man for element in test_list: verwenden.
Dieser Code durchläuft jedes Element in test_list und gibt es auf der Konsole aus.
'''
# Alle Elemente vom Array ausgeben
for element in test_list:
    print(element)

# ---------------------------------------------------------------------

'''
Um alle Elemente der for-Schleife durchzulaufen und den Index jedes Elements zu erhalten, 
kann man enumerate() verwenden. enumerate() gibt ein Tuple zurück, das den Index und das Element enthält.
'''

# Alle Elemente mit Index ausgeben
for index, element in enumerate(test_list):
    print("Element at index ", index, " is ", element)

# ---------------------------------------------------------------------

# Iteration über die Elemente der Liste und Hinzufügen der Typinformation
test_list = [1, 1.0, '1.0']
output = "["

for element in test_list:
    output += " <" + type(element).__name__ + ": " + str(element) + ">,"
    
# Entfernen des letzten Kommas und Hinzufügen der abschließenden Klammer
output = output[:-1] + " ]"
print(output)

# ---------------------------------------------------------------------

# Iteration über die Elemente der Liste und Hinzufügen der Typinformation
output = []

for element in test_list:
    type_val_str = '<{}: {}>'.format(type(element).__name__, element)
    output.append(type_val_str)
    
output_str = "[ " + ", ".join(output) + " ]"

print(output_str)

# ---------------------------------------------------------------------

# Erstellen Sie gemäß des vorherigen Beispiels eine Liste mit Typenamen 
# für die Elemente in test_list.
type_names = [type(element).__name__ for element in test_list]
print(type_names)

# ---------------------------------------------------------------------

# Verwenden Sie dann die zip() Methode, um eine Liste von tuple Ojekten 
# der Form [(type_name,obj),...] zu erhalten.
type_value_tuples = list(zip(type_names, test_list))
print(type_value_tuples)

# ---------------------------------------------------------------------

# Verwenden Sie diese Liste mit einer list comprehension, um wieder eine Liste von strings der Form 
# `<obj_type_name, obj>` zu erzeugen. Das Ergebnis können Sie dann wieder mit `string.join()` ausgeben.
formatted_strings = ['<{}: {}>'.format(type_name, value) for type_name, value in type_value_tuples]
output_str = "[ " + ", ".join(formatted_strings) + " ]"

print(output_str)