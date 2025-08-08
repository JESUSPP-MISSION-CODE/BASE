# save as generate_sample_data.py
import numpy as np

# Generate a sine wave with noise
t = np.linspace(0, 10, 1000)
signal = np.sin(2 * np.pi * 1 * t) + 0.2 * np.random.randn(len(t))

with open("example_signal.txt", "w") as f:
    for i in range(len(t)):
        f.write(f"{t[i]},{signal[i]}\n")