"""Musterloesung Aufgabe 3: Auswahl mit Bool'schen Variablen."""

import matplotlib.pyplot as plt
import pandas as pd


def read_force_emg(filename):
    """Liest die Kraft-/EMG-Daten als DataFrame ein."""
    return pd.read_csv(filename, sep=" ", comment="%", skipfooter=2, engine="python")


if __name__ == "__main__":
    threshold = 200  # N
    df = read_force_emg("force_emg.dat")
    dt = df["time"][1] - df["time"][0]

    active = df["force"] > threshold          # Bool'sche Variable
    n_active = active.sum()
    first_time = df["time"][active].iloc[0]
    emg_active = df["emg"][active].mean()
    emg_rest = df["emg"][~active].mean()

    lines = [
        f"Samples above {threshold} N: {n_active}",
        f"Total time above threshold: {n_active * dt:.2f} s",
        f"Force first exceeds threshold at t = {first_time:.3f} s",
        f"Mean EMG (active / rest): {emg_active:.4f} / {emg_rest:.4f} mV",
        f"Ratio active/rest: {emg_active / emg_rest:.1f}",
    ]
    with open("force_emg_result.txt", "w", encoding="utf-8") as fh:
        for line in lines:
            print(line)
            fh.write(line + "\n")

    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
    axs[0].plot(df["time"], df["force"], label="force")
    axs[0].plot(df["time"][active], df["force"][active], "r.", ms=2, label=f"> {threshold} N")
    axs[0].axhline(threshold, color="k", ls="--")
    axs[0].set_ylabel("Force [N]")
    axs[0].legend()
    axs[1].plot(df["time"], df["emg"])
    axs[1].set_xlabel("Time [s]")
    axs[1].set_ylabel("EMG RMS [mV]")
    fig.suptitle("Isometric knee extension")
    plt.tight_layout()
    plt.savefig("force_emg.png", dpi=200)
    plt.show()
