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

def az_el_from_xyz(df, xcol, ycol, zcol, forward_minus_z=False, degrees=True, unwrap=True):
    x = df[xcol].to_numpy(dtype=float)
    y = df[ycol].to_numpy(dtype=float)
    z = df[zcol].to_numpy(dtype=float)
    if forward_minus_z:
        z = -z  # switch conventions if forward is -Z

    az = np.arctan2(x, z)#yaw: +right is positive
    el = np.arctan2(y, np.hypot(x, z))#pitch: +up is positive

    if unwrap:
        az = np.unwrap(az)
        el = np.unwrap(el)
    if degrees:
        az = np.degrees(az)
        el = np.degrees(el)

    #optional for now
    az = az - az.mean()
    el = el - el.mean()

    return pd.Series(az, index=df.index, name="azimuth"), \
           pd.Series(el, index=df.index, name="elevation")

def calculate_vor(eye_df, head_df):
    ts='Relative_Timestamp'
    e = eye_df[[ts, 'az_deg']].copy()
    h = head_df[[ts, 'Head_Rotation_Y']].copy()

    # Inner join keeps only timestamps present in BOTH
    m = pd.merge(e, h, on=ts, how='inner', suffixes=('_eye', '_head'))
    # Build the columns you want
    m['eye_az_div2'] = m['az_deg'] / 2.0
    m['head_deg'] = np.rad2deg(m['Head_Rotation_Y'])
    # Avoid divide-by-zero for the ratio
    m = m.replace([np.inf, -np.inf], np.nan).dropna(subset=['head_deg'])
    m['vor_ratio'] = m['eye_az_div2'] / m['head_deg']
    return m

def _apply_sav_gol(df,col):
    df[col] = savgol_filter(df[col],window_length=31,polyorder=2)
    return df

def plot_vor(head_data, eye_data):
    ""
    'Left_Eye_Gaze_Position_X', 'Left_Eye_Gaze_Position_Y', 'Left_Eye_Gaze_Position_Z'
    ""
    az, el = az_el_from_xyz(
        eye_data,
        'Left_Eye_Gaze_Position_X',
        'Left_Eye_Gaze_Position_Y',
        'Left_Eye_Gaze_Position_Z',
        forward_minus_z=False,   # set True if your system uses -Z forward
        degrees=True,
        unwrap=True
    )
    eye_data['az_deg'], eye_data['el_deg'] = az, el
    plt.plot(eye_data['Relative_Timestamp'], az / 2, label='Eye azimuth (deg)')
    plt.plot(head_data['Relative_Timestamp'], np.rad2deg(head_data['Head_Rotation_Y']), label='Head (deg)')
    vor_df = _apply_sav_gol(calculate_vor(eye_data,head_data),'vor_ratio')
    print(vor_df['vor_ratio'].describe())
    plt.plot(vor_df['Relative_Timestamp'], vor_df['vor_ratio'], label='VOR (deg)')
    # plt.plot(eye_data['Relative_Timestamp'], el, label='Eye elevation (deg)')
    plt.legend(); plt.xlabel('Time'); plt.ylabel('Degrees'); plt.show()