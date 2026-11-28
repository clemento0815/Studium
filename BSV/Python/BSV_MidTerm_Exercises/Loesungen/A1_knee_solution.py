"""Musterloesung Aufgabe 1: Kniewinkel glaetten und ableiten."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def read_data(filename):
    """Liest Zeit und Winkel ein und gibt beide als Vektoren zurueck."""
    data = np.loadtxt(filename, skiprows=4)
    return data[:, 0], data[:, 1]


if __name__ == "__main__":
    time, angle = read_data("knee_angle.txt")
    dt = time[1] - time[0]

    # FIR-Filter (Savitzky-Golay): glaetten und 1. Ableitung
    angle_smooth = signal.savgol_filter(angle, window_length=21, polyorder=3)
    velocity = signal.savgol_filter(angle, window_length=21, polyorder=3, deriv=1, delta=dt)

    idx = np.argmax(velocity)
    text = f"Maximum angular velocity: {velocity[idx]:.1f} deg/s at t = {time[idx]:.2f} s"
    print(text)
    with open("knee_results.txt", "w", encoding="utf-8") as fh:
        fh.write(text + "\n")

    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
    axs[0].plot(time, angle, ".", ms=3, label="raw")
    axs[0].plot(time, angle_smooth, label="smoothed")
    axs[0].set_ylabel("Knee angle [deg]")
    axs[0].legend()
    axs[1].plot(time, velocity)
    axs[1].plot(time[idx], velocity[idx], "r*", ms=12)
    axs[1].set_xlabel("Time [s]")
    axs[1].set_ylabel("Angular velocity [deg/s]")
    fig.suptitle("Knee flexion during walking")
    plt.tight_layout()
    plt.savefig("knee_velocity.png", dpi=200)
    plt.show()
