"""Musterloesung Aufgabe 4: Funktionen fuer die Sprunganalyse (Modul)."""

import numpy as np

G = 9.81  # m/s^2


def body_weight(force, fs, t_quiet=1.0):
    """Mittelwert und Standardabweichung der Kraft im ruhigen Stand."""
    quiet = force[: int(t_quiet * fs)]
    return np.mean(quiet), np.std(quiet)


def flight_phase(force, fs, threshold=20):
    """Flugzeit sowie Start- und Endindex der Flugphase."""
    idx = np.where(force < threshold)[0]
    start, end = idx[0], idx[-1]
    return (end - start + 1) / fs, start, end


def jump_height(flight_time):
    """Sprunghoehe in m aus der Flugzeit: h = g * t^2 / 8."""
    return G * flight_time**2 / 8


if __name__ == "__main__":
    # Selbsttest: 0.5 s Flugzeit muss ca. 0.307 m ergeben
    print(f"Test jump_height(0.5) = {jump_height(0.5):.3f} m")
