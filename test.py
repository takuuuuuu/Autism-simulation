import matplotlib.pyplot as plt
import numpy as np

# Data for the boxplot
data = [
    [6.5, 1.5, 2.5, 5, 6, 6.5, 5.5, 4.5, 4, 4, 5, 4.5, 3.5, 6, 5],
    [4.7, 2, 2, 2.7, 3, 3.3, 3.7, 4, 4.3, 3, 4, 5, 4.7, 4.7, 4],
    [6, 2.5, 2, 4, 4, 4.5, 3, 3.5, 5, 5.5, 5, 3, 2.5, 2, 3.5],
    [5.3, 3.3, 2.3, 2, 3, 3.7, 3, 3.3, 4, 4.3, 3, 5, 5, 4.7, 4],
    [6, 7, 3, 3, 5, 4, 4.3, 5.3, 6.3, 6, 5.7, 3.7, 4.3, 3.7, 4.3]
]

# Labels for the x-axis
labels = ['Safety', 'Social Belonging', 'Esteem Needs', 'Meaning and Growth', 'Mental Health']

# Create the boxplot
plt.boxplot(
    data,
    patch_artist=True,  # Fill the boxes with color
    boxprops=dict(facecolor='#3C9566', color='black', linewidth=1),  # Box color and line width
    whiskerprops=dict(color='black', linewidth=1),  # Whiskers color and line width
    capprops=dict(color='black', linewidth=1),  # Caps color and line width
    flierprops=dict(marker='.', color='red', markersize=10),  # Outliers color and size
    medianprops=dict(color='red', linewidth=1)  # Median line color and thickness
)

# Set x-axis labels and title
plt.xticks(np.arange(1, len(labels) + 1), labels,fontsize=6, fontweight='bold')
plt.yticks(fontweight='bold')
plt.ylim(-5, 8)

# Adjust line width and tick parameters
plt.tick_params(axis='both', width=1)

# Display the boxplot
plt.show()