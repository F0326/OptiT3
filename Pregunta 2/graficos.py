import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

# Puntos del conjunto W
points = np.array([
    [1, 1],  # A
    [2, 5],  # B
    [3, 3],  # C
    [4, 3]   # D
])

# Graficar los puntos
plt.plot(points[:,0], points[:,1], 'o', label='Puntos de W')

# Anotar los puntos
labels = ['A (1,1)', 'B (2,5)', 'C (3,3)', 'D (4,3)']
for i, txt in enumerate(labels):
    plt.annotate(txt, (points[i][0]+0.1, points[i][1]+0.1))

plt.xlim(0, 5)
plt.ylim(0, 6)
plt.title("Puntos y Envoltura Convexa de W")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()