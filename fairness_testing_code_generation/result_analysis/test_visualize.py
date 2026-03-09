import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define data
x_axis = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3]  # Added extra point at x=3
y_axis = [0.0, 0.2, 0.4, 0.6, 0.8, 0.1, 0.0, 0.2, 0.4, 0.6, 0.8, 0.1, 0.5]  # Added y-axis value for extra point

# Point data (colors and sizes can be adjusted)
point_size = 150
point_color1 = 'red'
point_color2 = 'blue'

# Data categories for legend
categories = ['Education' , 'Gender']

# Create the scatter plot
plt.figure(figsize=(8, 6))

# Plot background data (all points) without label
plt.scatter(x_axis, y_axis, marker='o', alpha=0.5, color='gray')  # Adjust marker and transparency

# Plot highlighted points with categories
plt.scatter(x_axis[1], y_axis[1], s=point_size, color=point_color1, label=categories[0])
plt.scatter(x_axis[1] + 0.1, y_axis[1], s=point_size * 2, color=point_color2, label=categories[1])
plt.scatter(x_axis[2], y_axis[2], s=point_size, color=point_color1, label=categories[0])  # Added for extra point

# Customize plot elements
plt.xlabel('Models')  # Rename x-axis label
plt.ylabel('Temperature')  # Rename y-axis label
plt.title('Scatter Plot with Highlighted Points')
plt.xticks([1, 2, 3], ['X1', 'X2', 'X3'])  # Updated x-axis ticks for new point
plt.grid(True)

# Add legend (without background data label)
# legend = plt.legend(title='Categories')


red_patch = mpatches.Patch(color='red', label='The red data')
blue_patch = mpatches.Patch(color='blue', label='The blue data')

# plt.legend(handles=[red_patch, blue_patch])
plt.legend(handles=[red_patch, blue_patch])

# Set equal marker size for legend entries (optional)
# for handle in legend.legend_handles:
#     handle.set_sizes([64])  # Adjust size as needed

# Rest of the code (tight_layout, show)
plt.tight_layout()
plt.show()
