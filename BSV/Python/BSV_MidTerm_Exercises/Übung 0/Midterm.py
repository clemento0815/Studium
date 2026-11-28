"""Maxima"""

# author: Clemens Loher
# date: 2026-11-28

# Import standard packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal

# Daten einlesen Funktion definieren


def daten_einlesen(dateipfad):
    """Liest die Daten aus einer csv-Datei ein und gibt sie als Pandas DataFrame zurück."""
    return pd.read_csv(dateipfad, delimiter=":", skipfooter=2, engine="python")


def vector_length(x, y, z):
    """Berechnet die Länge des Vektors anhand x y und z"""
    length = np.sqrt(x**2 + y**2 + z**2)
    return length


# Dateipfad in Variable speichern
dateipfad = "maxima.csv"

# Funktionsaufruf
df = daten_einlesen(dateipfad)

# ersten 10 zeilen und letzten 10 Zeilen und Shape anzeigen
print(df.shape)
print(df.head(10))
print(df.tail(10))

# data in ein np.array umwandeln
data = np.array(df)
print(data.shape)

laengen = vector_length(df["x"], df["y"], df["z"])
print(laengen.shape)


# Maximum herausfinden
maximum = np.max(laengen)
print(maximum)

# Ort des Maximums herausfinden
where_maximum = np.where(maximum == laengen)[0][0]
print(where_maximum)

# Fensterarray
window = data[where_maximum - 3 : where_maximum + 4, :]
print(window.shape)

# Mittelwert berechnen
mean_3Dposition = np.mean(window, axis=0)
print(mean_3Dposition)

# Ergenis rausschreiben
print(
    f"Position about the maximum: [{mean_3Dposition[0]:4.2f}/{mean_3Dposition[1]:4.2f}/{mean_3Dposition[2]:4.2f}]"
)
out_file = "maxima_result.txt"
with open(out_file, "w") as fh:
    fh.write(
        f"Position about the maximum: [{mean_3Dposition[0]:4.2f}/{mean_3Dposition[1]:4.2f}/{mean_3Dposition[2]:4.2f}]"
    )

print(f"results have been saved to {out_file}")
