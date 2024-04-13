import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Initialize empty lists for x and y data
x_data = []
y_data = []


# Define the update function to be called by the animation
def update(frame):
    x_data.append(frame)
    y_data.append(np.random.normal(0, 1))  # Simulate random data
    line.set_data(x_data, y_data)
    ax.relim()
    ax.autoscale_view()
    return line


# Create the animation
ani = FuncAnimation(fig, update, frames=np.linspace(0, 10, 100), interval=100)

# Show the plot
plt.show()
