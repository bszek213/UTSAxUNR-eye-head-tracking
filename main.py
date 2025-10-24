from utils import *

def main():
    eye_data = load_data("STEVEN100725C_1/Subject_STEVEN100725C_2025-10-07_17-06-49_1_Gaze Stability & Dynamic Visual Acuity_21M_3056_EyeTracking.csv")
    head_data = load_data("STEVEN100725C_1/Subject_STEVEN100725C_2025-10-07_17-06-49_1_Gaze Stability & Dynamic Visual Acuity_21M_3056_HeadTracking.csv")
    print(head_data.columns.tolist())
    print('========')
    print(eye_data.columns.tolist())
    print(eye_data['Relative_Timestamp'])
    plot_head_data(head_data,eye_data)
    

if __name__ == "__main__":
    main()