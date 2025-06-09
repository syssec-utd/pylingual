"""
========================
MATPLOTLIB **UNCHAINED**
========================

Comparative path demonstration of frequency from a fake signal of a pulsar
(mostly known because of the cover for Joy Division's Unknown Pleasures).

Author: Nicolas P. Rougier

Output generated via `matplotlib.animation.Animation.to_jshtml`.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
np.random.seed(19680801)
fig = plt.figure(figsize=(8, 8), facecolor='black')
ax = plt.subplot(frameon=False)
data = np.random.uniform(0, 1, (64, 75))
X = np.linspace(-1, 1, data.shape[-1])
G = 1.5 * np.exp(-4 * X ** 2)
lines = []
for i in range(len(data)):
    xscale = 1 - i / 200.0
    lw = 1.5 - i / 100.0
    (line,) = ax.plot(xscale * X, i + G * data[i], color='w', lw=lw)
    lines.append(line)
ax.set_ylim(-1, 70)
ax.set_xticks([])
ax.set_yticks([])
ax.text(0.5, 1.0, 'MATPLOTLIB ', transform=ax.transAxes, ha='right', va='bottom', color='w', family='sans-serif', fontweight='light', fontsize=16)
ax.text(0.5, 1.0, 'UNCHAINED', transform=ax.transAxes, ha='left', va='bottom', color='w', family='sans-serif', fontweight='bold', fontsize=16)

def update(*args):
    data[:, 1:] = data[:, :-1]
    data[:, 0] = np.random.uniform(0, 1, len(data))
    for i in range(len(data)):
        lines[i].set_ydata(i + G * data[i])
    return lines
anim = animation.FuncAnimation(fig, update, interval=10, save_count=100)
plt.show()