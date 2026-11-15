"""EMG Signals Event-Detection"""

# author: Clemens Loher
# date: 2026-11-03

# Import standard packages
import matplotlib.pyplot as plt
import numpy as np
from mat4py import loadmat
from scipy import signal

# loading matlab data
loaded_data = loadmat("S1_A1_E1.mat")
print(loaded_data.keys())
print(f"Exercise: {loaded_data['exercise']}")
# Ex 1=Ex A has 12 Stim-Steps
# Ex 2=Ex B has 17 Stim-Steps
# Ex 3=Ex C has 23 Stim-Steps


# printing name and shape of each variable
for name, value in loaded_data.items():
    arr = np.array(value)
    print(f"{name:15s}: {arr.shape}")

stimulus = np.array(loaded_data["stimulus"]).ravel()  # (N, 1) -> (N,)

# plotting the stimulus signal
rate = 100  # sampling rate in Hz
time = np.arange(len(stimulus)) / rate  # time vector in seconds

plt.figure(figsize=(12, 4))
plt.plot(time, stimulus)
plt.xlabel("Time [s]")
plt.ylabel("Stimulus")
plt.title("Stimulus Signal")
plt.tight_layout()
plt.show()

# Comparison with the NinaPro website:
# The stimulus contains 12 movements (1-12), each repeated 10 times.
# This corresponds to Exercise A (12 finger movements).
# In the section 100-150 s, movement 2 ("Index extension") is performed.

# loading the EMG signal
emg = np.array(loaded_data["emg"])  # shape (N, 10): one column per electrode

# total EMG: sum of the absolute values of all 10 channels
total_emg = np.sum(np.abs(emg), axis=1)

plt.figure(figsize=(12, 4))
plt.plot(time, total_emg)
plt.xlabel("Time [s]")
plt.ylabel("Total EMG")
plt.title("EMG Signal")
plt.tight_layout()
plt.show()

# cutting out 100 to 150 seconds of the EMG signal (logical indexing)
my_domain = (time >= 100) & (time < 150)
section = total_emg[my_domain]
t_section = time[my_domain] - 100  # time relative to the start of the section

# smoothing the signal (Savitzky-Golay filter, 0.5 s window, see Chapter 5)
# Without smoothing, the noisy signal crosses the threshold many times
# during one movement and produces 17-20 "movements" instead of 6.
smoothed = signal.savgol_filter(section, window_length=51, polyorder=1)

# threshold: set manually after inspecting the data
# rest level is about 0.05, the peaks are above 1.4
threshold = 0.2
is_active = smoothed > threshold  # logical vector

# onsets and offsets with np.diff (see Listing 6.2 in the book)
start_stop = np.diff(is_active * 1)  # "*1": convert boolean to numerical
onsets = np.where(start_stop == 1)[0]
offsets = np.where(start_stop == -1)[0]

# printing the start and end times of the movements
print(f"{len(onsets)} movements found:")
for on, off in zip(onsets, offsets):
    print(f"  {t_section[on]:5.2f} s - {t_section[off]:5.2f} s")

# indicating the range of the movements, together with the stimulus
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(9, 6))

# top: stimulus (instruction)
axs[0].plot(t_section, stimulus[my_domain], color="C1")
axs[0].set_ylabel("Stimulus")
axs[0].set_title("Stimulus (top) and total EMG (bottom)")

# bottom: total EMG with the detected movements
axs[1].plot(t_section, section, lw=0.8)
axs[1].axhline(threshold, ls="dotted", color="C1")
for on, off in zip(onsets, offsets):
    axs[1].axvspan(t_section[on], t_section[off], color="0.9", zorder=0)
axs[1].set_ylabel("Total EMG")
axs[1].set_xlabel("Time (s)")

for ax in axs:
    ax.margins(x=0)

plt.tight_layout()
plt.show()
