from utils import *

def main():
    eye_data = load_data("STEVEN100725C_1/Subject_STEVEN100725C_2025-10-07_17-06-49_1_Gaze Stability & Dynamic Visual Acuity_21M_3056_EyeTracking.csv")
    head_data = load_data("STEVEN100725C_1/Subject_STEVEN100725C_2025-10-07_17-06-49_1_Gaze Stability & Dynamic Visual Acuity_21M_3056_HeadTracking.csv")
    
    eye_data_rod_1 = load_data("STEVEN100725C_1/Subject_STEVEN100725C_2025-10-07_17-05-57_1_Rod and Frame Pretest_201D_7696_EyeTracking.csv")
    eye_data_rod_2 = load_data("STEVEN100725C_1/Subject_STEVEN100725C_2025-10-07_17-21-44_1_Rod and Frame Postest_202I_1145_EyeTracking.csv")
    head1 = load_data("STEVEN100725C_1/Subject_STEVEN100725C_2025-10-07_17-05-57_1_Rod and Frame Pretest_201D_7696_HeadTracking.csv")
    head2 = load_data("STEVEN100725C_1/Subject_STEVEN100725C_2025-10-07_17-21-44_1_Rod and Frame Postest_202I_1145_HeadTracking.csv")
    plot_head_data(head1, head2)
    # print(head_data.columns.tolist())
    print('========')
    # print(eye_data_smooth.columns.tolist())
    print(eye_data['Relative_Timestamp'])

    plot_smooth(eye_data_rod_1,eye_data_rod_2)
    plot_vor(head_data,eye_data)

    # plot_head_data(head_data,eye_data)

if __name__ == "__main__":
    main()