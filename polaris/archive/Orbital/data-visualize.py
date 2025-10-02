import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Function to load data from a CSV file and compute angular velocity and acceleration for Y-axis
def load_and_compute_angular_data_y(filename):
    data = pd.read_csv(filename)

    time = data['Time']  # Assuming time is in seconds or needs conversion
    gyro_y = data['Gyro Y']

    # Convert Time from arbitrary units to seconds (if needed)
    # Uncomment the next line if time is in milliseconds
    # time = time / 1000 

    # Angular velocity for Y-axis (Gyroscope data gives angular velocity directly)
    angular_velocity_y = gyro_y / 16000

    # Calculate angular acceleration as the derivative of angular velocity over time
    angular_acceleration_y = np.gradient(angular_velocity_y, time)

    # Calculate average angular velocity and average time
    avg_angular_velocity = np.mean(angular_velocity_y)
    avg_time_interval = np.mean(np.diff(time))

    # Calculate average derivative (average angular acceleration)
    average_derivative = np.mean(angular_acceleration_y)

    return time, angular_velocity_y, angular_acceleration_y, avg_angular_velocity, avg_time_interval, average_derivative

# List of filenames to load
filenames = ['test_data/left_2024-09-20_14-41-23.csv', 
             'test_data/left_2024-09-20_14-41-59.csv', 
             'test_data/left_2024-09-20_14-42-18.csv']  

# Plotting
plt.figure(figsize=(12, 8))

# Plot for Angular Velocity (Y-axis only)
plt.subplot(2, 1, 1)
for filename in filenames:
    time, angular_velocity_y, _, avg_angular_velocity, avg_time_interval, average_derivative = load_and_compute_angular_data_y(filename)
    
    plt.plot(time, angular_velocity_y, label=f'{filename} - Angular Velocity Y')

plt.title('Angular Velocity Y (Multiple Files)')
plt.xlabel('Time (s)')
plt.ylabel('Angular Velocity Y (deg/s)')
plt.legend()

# Plot for Angular Acceleration (Y-axis only)
plt.subplot(2, 1, 2)
for filename in filenames:
    time, _, angular_acceleration_y, _, _, _ = load_and_compute_angular_data_y(filename)
    
    plt.plot(time, angular_acceleration_y, label=f'{filename} - Angular Acceleration Y')

plt.title('Linear Acceleration Y (Multiple Files)')
plt.xlabel('Time (s)')
plt.ylabel('Linear Acceleration Y')
plt.legend()

plt.tight_layout()
plt.show()
