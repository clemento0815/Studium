"""Musterloesung Aufgabe 4: Hauptskript."""

import matplotlib.pyplot as plt
import numpy as np

from A4_jump_functions import G, body_weight, flight_phase, jump_height

if __name__ == "__main__":
    fs = 1000
    force = np.loadtxt("jump_force.txt", skiprows=1)
    time = np.arange(len(force)) / fs

    bw_mean, bw_std = body_weight(force, fs)
    t_flight, i_start, i_end = flight_phase(force, fs)
    h = jump_height(t_flight)

    lines = [
        f"Body weight: {bw_mean:.1f} +/- {bw_std:.1f} N",
        f"Body mass: {bw_mean / G:.1f} kg",
        f"Flight time: {t_flight:.3f} s",
        f"Jump height: {h * 100:.1f} cm",
    ]
    with open("jump_result.txt", "w", encoding="utf-8") as fh:
        for line in lines:
            print(line)
            fh.write(line + "\n")

    plt.plot(time, force)
    plt.axvspan(time[i_start], time[i_end], color="orange", alpha=0.3, label="flight phase")
    plt.axhline(bw_mean, color="k", ls="--", label="body weight")
    plt.xlabel("Time [s]")
    plt.ylabel("Vertical force [N]")
    plt.title("Countermovement jump")
    plt.legend()
    plt.savefig("jump.png", dpi=200)
    plt.show()
