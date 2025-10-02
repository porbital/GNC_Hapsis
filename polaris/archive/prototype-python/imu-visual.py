from time import sleep
from BMI160_i2c import Driver
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize the sensor
print('Trying to initialize the sensor...')
sensor = Driver(0x68)  # change address if needed
print('Initialization done')

# Create lists to store data
gx_data, gy_data, gz_data, ax_data, ay_data, az_data = [], [], [], [], [], []

# Set up the plot
fig, axs = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle('IMU Data Visualization')
axs[0].set_ylabel('Gyro Values')
axs[1].set_ylabel('Accelerometer Values')
axs[1].set_xlabel('Time (s)')  # Adjusted the label to represent time in seconds

# Function to update the plot in real-time
def update_plot(frame):
    global gx_data, gy_data, gz_data, ax_data, ay_data, az_data

    data = sensor.getMotion6()
    gx_data.append(data[0])
    gy_data.append(data[1])
    gz_data.append(data[2])
    ax_data.append(data[3])
    ay_data.append(data[4])
    az_data.append(data[5])

    # Limit the number of data points to display
    max_data_points = 500  # Increased the maximum data points to accommodate faster updates
    gx_data = gx_data[-max_data_points:]
    gy_data = gy_data[-max_data_points:]
    gz_data = gz_data[-max_data_points:]
    ax_data = ax_data[-max_data_points:]
    ay_data = ay_data[-max_data_points:]
    az_data = az_data[-max_data_points:]

    # Calculate time axis based on the number of data points and the update interval (0.01 seconds)
    time_axis = [i * 0.01 for i in range(len(gx_data))]

    axs[0].clear()
    axs[1].clear()

    axs[0].plot(time_axis, gx_data, label='gx')
    axs[0].plot(time_axis, gy_data, label='gy')
    axs[0].plot(time_axis, gz_data, label='gz')
    axs[0].legend()

    axs[1].plot(time_axis, ax_data, label='ax')
    axs[1].plot(time_axis, ay_data, label='ay')
    axs[1].plot(time_axis, az_data, label='az')
    axs[1].legend()

    # Set x-axis limits to display the last 10 seconds of data
    axs[0].set_xlim(max(0, time_axis[-1] - 10), time_axis[-1])
    axs[1].set_xlim(max(0, time_axis[-1] - 10), time_axis[-1])

# Create an animation with a shorter interval (0.01 seconds)
ani = FuncAnimation(fig, update_plot, blit=False, interval=10)

plt.show()

