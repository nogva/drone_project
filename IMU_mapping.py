import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re

#TODO Finne ut hva vi må gjøre med tyngdekraften
#TODO Sjekke om disse stemmer eller ikke.. 

def parse_imu_data(imu_data):
    sensors = ['accelerometer', 'gyroscope', 'magnetometer']
    imu_dict = {}
    for sensor in sensors:
        pattern = re.compile(r'{} \{{\s*x:\s*(-?\d+\.?\d*)\s*y:\s*(-?\d+\.?\d*)\s*z:\s*(-?\d+\.?\d*)\s*\}}'.format(sensor))
        match = pattern.search(imu_data)
        if match:
            imu_dict[sensor] = {'x': float(match.group(1)), 'y': float(match.group(2)), 'z': float(match.group(3))}
    return imu_dict

df = pd.read_csv('telemetry_data.csv', converters={'IMU1Data': parse_imu_data, 'IMU2Data': parse_imu_data})
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

dt = 0.01  # 10 ms mellom hver IMU oppdatering

def compute_velocity_position(acc_data, dt):
    acc_data[:, 2] -= 0.981 # TODO Hva skal denne være? 
    velocity = np.cumsum(acc_data * dt, axis=0)
    position = np.cumsum(velocity * dt, axis=0)
    return velocity, position

def prepare_data(imu_data):
    return np.array([list(x['accelerometer'].values()) for x in imu_data if 'accelerometer' in x])

# Forbered data
acc_data1 = prepare_data(df['IMU1Data'])
acc_data2 = prepare_data(df['IMU2Data'])

# Beregn hastighet og posisjon
velocity1, position1 = compute_velocity_position(acc_data1, dt)
velocity2, position2 = compute_velocity_position(acc_data2, dt)

# Trim timestamps for å matche lengden på acc_data, velocity og position
timestamps = df['Timestamp'].values[:len(acc_data1)]

def plot_imu_data(imu_label, timestamps, acc_data, velocity_data, position_data, filename):
    # Ensure the lengths match
    min_length = min(len(timestamps), len(acc_data), len(velocity_data), len(position_data))
    timestamps = timestamps[:min_length]
    acc_data = acc_data[:min_length]
    velocity_data = velocity_data[:min_length]
    position_data = position_data[:min_length]
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    fig.suptitle(f'{imu_label} - IMU Data Analysis')

    # Acceleration plot
    axs[0].plot(timestamps, acc_data[:, 0], label='Acc X', linestyle='-', color='r')
    axs[0].plot(timestamps, acc_data[:, 1], label='Acc Y', linestyle='-', color='g')
    axs[0].plot(timestamps, acc_data[:, 2], label='Acc Z', linestyle='-', color='b')
    axs[0].set_title('Acceleration')
    axs[0].set_ylabel('Acceleration (m/s²)')
    axs[0].legend()

    # Velocity plot
    axs[1].plot(timestamps, velocity_data[:, 0], label='Vel X', linestyle='-', color='r')
    axs[1].plot(timestamps, velocity_data[:, 1], label='Vel Y', linestyle='-', color='g')
    axs[1].plot(timestamps, velocity_data[:, 2], label='Vel Z', linestyle='-', color='b')
    axs[1].set_title('Velocity')
    axs[1].set_ylabel('Velocity (m/s)')
    axs[1].legend()

    # Position plot
    axs[2].plot(timestamps, position_data[:, 0], label='Pos X', linestyle='-', color='r')
    axs[2].plot(timestamps, position_data[:, 1], label='Pos Y', linestyle='-', color='g')
    axs[2].plot(timestamps, position_data[:, 2], label='Pos Z', linestyle='-', color='b')
    axs[2].set_title('Position')
    axs[2].set_ylabel('Position (m)')
    axs[2].set_xlabel('Timestamp')
    axs[2].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(filename)  # Lagre figuren til fil
    plt.show()

def plot_3d_position(position1, position2):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(position1[:, 0], position1[:, 1], position1[:, 2], label='IMU1', linestyle='-', color='r')
    ax.plot(position2[:, 0], position2[:, 1], position2[:, 2], label='IMU2', linestyle='-', color='b')
    
    ax.set_title('3D Spatial Position of IMU1 and IMU2')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_zlabel('Z Position (m)')
    ax.legend()
    
    plt.show()

# Juster lengden på acc_data for å matche timestamps
acc_data1 = acc_data1[:len(timestamps)]
acc_data2 = acc_data2[:len(timestamps)]

# Plot og lagre data for IMU1
plot_imu_data('IMU1', timestamps, acc_data1, velocity1, position1, 'IMU1_Data_Analysis.png')

# Plot og lagre data for IMU2
plot_imu_data('IMU2', timestamps, acc_data2, velocity2, position2, 'IMU2_Data_Analysis.png')

# Plot 3D spatial position
plot_3d_position(position1, position2)