"""
Statistics: hip implants, random numbers, comparison of two groups
solved with Claude AI
"""

# author: Clemens Loher
# date: 2026-11-23

# Import standard packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal, stats

# %% 0.1 First steps: random number generator with a fixed seed
rng = np.random.default_rng(12345)

# %% 1 Hip implants
# Implants may deviate by up to +/- 1 mm from the specified size.
# Only 1 out of 1000 (0.1 %) may lie outside this range.
# -> 0.05 % on each side (too big / too small)  -> two-sided
tolerance = 1  # [mm]
alpha = 1 / 1000

# How many standard deviations correspond to 99.95 % of the normal distribution?
# (ppf = "percentile point function", see Chapter 7.2 in the book)
z = stats.norm().ppf(1 - alpha / 2)

# tolerance = z * sd  ->  sd = tolerance / z
sd_required = tolerance / z

print("1 Hip implants")
print(f"  z-value for 99.9 %: {z:.2f} SD")
print(f"  Required standard deviation: {sd_required:.3f} mm\n")

# %% 2 Random numbers
# 1000 normally distributed values: mean 175, SD 12.5
data = rng.normal(loc=175, scale=12.5, size=1000)

print("2 Random numbers")
print(f"  mean = {np.mean(data):.2f}, SD = {np.std(data, ddof=1):.2f}")

# Histogram and boxplot
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
axs[0].hist(data, bins=25)
axs[0].set_xlabel("Value")
axs[0].set_ylabel("Counts")
axs[0].set_title("Histogram")

axs[1].boxplot(data, sym="*")
axs[1].set_ylabel("Value")
axs[1].set_title("Boxplot")
plt.tight_layout()
plt.show()

# 3x2 matrix of integers between 0 and 9 (the upper limit 10 is excluded!)
int_matrix = rng.integers(0, 10, size=(3, 2))
print(f"  3x2 integers 0-9:\n{int_matrix}")

# 3x2 matrix of different integers (each number occurs only once)
diff_matrix = rng.choice(10, size=(3, 2), replace=False)
print(f"  3x2 different integers:\n{diff_matrix}")

# Same data set as the first time: reset the generator to the same seed
rng = np.random.default_rng(12345)
data_again = rng.normal(loc=175, scale=12.5, size=1000)
print(f"  Same data as the first time? {np.all(data == data_again)}\n")

# %% 3 Compare two groups
# Assumption: the file contains two columns, one per group
in_file = "data_to_compare.txt"
values = np.loadtxt(in_file)
group1 = values[:, 0]
group2 = values[:, 1]

# Visual comparison: both groups as boxplots next to each other
plt.figure()
plt.boxplot([group1, group2], sym="*")
plt.xticks([1, 2], ["Group 1", "Group 2"])
plt.ylabel("Height")
plt.title("Comparison of the two groups")
plt.show()

# Unpaired T-test (two independent groups, see Chapter 7.3.4 in the book)
t, p = stats.ttest_ind(group1, group2)

# Numerical comparison
result = (
    f"Group 1: n = {len(group1)}, mean = {np.mean(group1):.2f}, "
    f"SD = {np.std(group1, ddof=1):.2f}\n"
    f"Group 2: n = {len(group2)}, mean = {np.mean(group2):.2f}, "
    f"SD = {np.std(group2, ddof=1):.2f}\n"
    f"Difference of the means: {np.mean(group1) - np.mean(group2):.2f}\n"
    f"Unpaired T-test: t = {t:.3f}, p = {p:.4f}\n"
)
if p < 0.05:
    result += "The two groups are significantly different (p < 0.05).\n"
else:
    result += "The two groups are not significantly different (p >= 0.05).\n"

print("3 Compare two groups")
print(result)

# Write the result to a text file
out_file = "differences.txt"
with open(out_file, "w") as fh:
    fh.write(result)
print(f"Result written to {out_file}")
