"""Musterloesung Aufgabe 2: Rotation und Translation von 3D-Markerdaten."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def read_markers(filename):
    """Liest die Markerdaten (Semikolon, Dezimalkomma) als NumPy-Array ein."""
    df = pd.read_csv(filename, sep=";", decimal=",")
    return df.to_numpy()


def transform(points, angle_deg, translation):
    """Rotiert Punkte (Zeilen) um die z-Achse und verschiebt sie anschliessend."""
    a = np.deg2rad(angle_deg)
    R = np.array([[np.cos(a), -np.sin(a), 0],
                  [np.sin(a),  np.cos(a), 0],
                  [0,          0,         1]])
    return points @ R.T + translation


if __name__ == "__main__":
    markers = read_markers("markers.csv")
    moved = transform(markers, 30, np.array([100, -50, 20]))

    last = moved[-150:]
    mean_v, min_v, max_v = last.mean(axis=0), last.min(axis=0), last.max(axis=0)

    lines = [
        f"Number of data points: {markers.shape[0]}",
        f"Mean of last 150 points: [{mean_v[0]:.1f}/{mean_v[1]:.1f}/{mean_v[2]:.1f}] mm",
        f"Min of last 150 points:  [{min_v[0]:.1f}/{min_v[1]:.1f}/{min_v[2]:.1f}] mm",
        f"Max of last 150 points:  [{max_v[0]:.1f}/{max_v[1]:.1f}/{max_v[2]:.1f}] mm",
    ]
    with open("markers_result.txt", "w", encoding="utf-8") as fh:
        for line in lines:
            print(line)
            fh.write(line + "\n")

    plt.plot(markers[:, 0], markers[:, 1], label="original")
    plt.plot(moved[:, 0], moved[:, 1], label="rotated + translated")
    plt.plot(last[:, 0], last[:, 1], "k.", ms=3, label="last 150 points")
    plt.axis("equal")
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.title("Marker trajectory (top view)")
    plt.legend()
    plt.savefig("markers.png", dpi=200)
    plt.show()
