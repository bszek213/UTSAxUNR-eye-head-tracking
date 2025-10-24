import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

def load_data(file_path):
    """Load data from a CSV file."""
    return pd.read_csv(file_path)

def velocity(data, time_column, position_column):
    dt = np.diff(data[time_column])
    dx = np.diff(data[position_column])
    velocity = dx / dt
    return np.concatenate(([0], velocity))

def smooth_velocity(velocity, window_length=51, polyorder=2):
    return savgol_filter(velocity, window_length, polyorder)

def plot_head_data(head_data, eye_data):
    plt.figure(figsize=(10, 6))
    ts = pd.to_datetime(head_data['UTC_Timestamp'])
    avg_dt_sec = ts.diff().dt.total_seconds().dropna()

    # time_diff_avg = np.mean(np.diff(eye_data['Relative_Timestamp']))
    # print(1/time_diff_avg)
    horz_eye_vel = velocity(eye_data, 'Relative_Timestamp', 'Left_Eye_Rotation_Y')
    horz_head_vel = velocity(head_data, 'Relative_Timestamp', 'Head_Rotation_Y')
    # plt.plot(head_data['Head_Rotation_X'], label='Head Angular movement X')
    # plt.plot(head_data['Head_Rotation_Y'], label='Head Angular movement Y')
    # plt.plot(head_data['Head_Rotation_Z'], label='Head Angular movement Z')
    plt.plot(np.rad2deg(horz_eye_vel), label='Eye Angular Velocity Y')
    plt.plot(np.rad2deg(horz_head_vel), label='Head Angular Velocity Y')

    plt.xlabel('Time')
    plt.ylabel('Angular Displacement (deg)')
    plt.title('Head Angular Velocity Over Time')
    plt.legend()
    plt.show()