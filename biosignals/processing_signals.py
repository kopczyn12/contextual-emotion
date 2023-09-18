import argparse
import os
import numpy as np
import biosppy
from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values, get_time_domain_features, get_frequency_domain_features, get_geometrical_features, get_poincare_plot_features, get_csi_cvi_features
import matplotlib.pyplot as plt
from pymongo import MongoClient
import pandas as pd
import nolds

def process_data(signal_data, sampling_rate):
    """
    Process the ECG data including R-peak detection, outlier removal, ectopic beat removal and interpolation of missing values.

    Args:
    signal_data (numpy.array): The ECG data
    sampling_rate (float): The sampling rate of the ECG data

    Returns:
    tuple: Contains results of the ECG data processing
    """
    out = biosppy.signals.ecg.ecg(signal_data, sampling_rate=sampling_rate, show=False)
    rr_intervals_list = np.diff(out["ts"][out['rpeaks']]) * 1000 
    
    # low_rri, high_rri - to change up to our tests
    rr_intervals_without_outliers = remove_outliers(rr_intervals=rr_intervals_list, low_rri=300, high_rri=2000)
    interpolated_rr_intervals = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,
                                                       interpolation_method="linear")
    nn_intervals_list = remove_ectopic_beats(rr_intervals=interpolated_rr_intervals, method="malik")
    interpolated_nn_intervals = interpolate_nan_values(rr_intervals=nn_intervals_list)

    return out, rr_intervals_list, rr_intervals_without_outliers, interpolated_rr_intervals, nn_intervals_list, interpolated_nn_intervals

def plot_ecg_and_r_peaks(ecg_data, out):
    """
    Plot the ECG data and highlight the detected R-peaks.

    Args:
    ecg_data (numpy.array): The ECG data.
    out (dict): The output from the R-peak detection algorithm. This should contain a key 'rpeaks' which maps to an array of indices.

    Returns:
    None
    """
    plt.figure()
    plt.plot(ecg_data, label='ECG Signal')
    plt.plot(out['rpeaks'], ecg_data[out['rpeaks']], 'ro', label='R-peaks')
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.title('ECG Signal with R-peaks')
    plt.legend()

def hrv_analysis(interpolated_nn_intervals, window_duration=270, step_size=30, email=''):
    """
    Perform Heart Rate Variability (HRV) analysis on the NN intervals.

    Args:
    interpolated_nn_intervals (numpy.array): The NN intervals after interpolation.
    window_duration (int, optional): The duration of each window for HRV analysis. Default is 270.
    step_size (int, optional): The step size for the sliding window. Default is 30.
    email (str, optional): The email of the user. Default is an empty string.

    Returns:
    tuple: Contains two lists: one for HR values and one for HRV indices.
    """
    num_intervals = len(interpolated_nn_intervals)
    epoch_intervals = int(window_duration)
    step_intervals = int(step_size)
    hrv_indices = []
    hr_values = []

    for i in range(0, num_intervals - epoch_intervals + step_intervals, step_intervals):
        epoch_nn_intervals = interpolated_nn_intervals[i:i + epoch_intervals]
        if len(epoch_nn_intervals) == 0:
            print(f"Empty nn_intervals for epoch {i}-{i + epoch_intervals}")
            continue
        try:
            time_domain_features = get_time_domain_features(epoch_nn_intervals)
            frequency_domain_features = get_frequency_domain_features(epoch_nn_intervals)
            poincare_plot_features = get_poincare_plot_features(epoch_nn_intervals)
            csi_cvi_features = get_csi_cvi_features(epoch_nn_intervals)
            
            # separate csv for hr
            epoch_hr = {}
            epoch_hr['mean_hr'] = time_domain_features['mean_hr']
            epoch_hr['user_email'] = email
            epoch_hr['epoch_index'] = i // step_intervals + 1
            hr_values.append(epoch_hr)

            #separate for hrv analysis
            epoch_hrv_indices = {}
            epoch_hrv_indices.update(time_domain_features)
            epoch_hrv_indices.update(frequency_domain_features)
            epoch_hrv_indices.update(poincare_plot_features)
            epoch_hrv_indices.update(csi_cvi_features)

            # calculate asymmetry of Poincare plot area index
            left_area = poincare_plot_features['sd1'] ** 2
            right_area = poincare_plot_features['sd2'] ** 2
            total_area = left_area + right_area
            asymmetry_index = abs(left_area - right_area) / total_area
            epoch_hrv_indices['C1d'] = asymmetry_index
            epoch_hrv_indices['C2d'] = csi_cvi_features['cvi']
            epoch_hrv_indices['C2a'] = csi_cvi_features['csi']
            hf_power = frequency_domain_features['hf']
            short_term_var_of_accelerations = hf_power / len(epoch_nn_intervals)
            epoch_hrv_indices['SD1a'] = short_term_var_of_accelerations
            epoch_nn_intervals = np.array(epoch_nn_intervals)
            deceleration_index = (epoch_nn_intervals[1:] - epoch_nn_intervals[:-1] > 50).sum() / len(epoch_nn_intervals)
            acceleration_index = (epoch_nn_intervals[1:] - epoch_nn_intervals[:-1] < -50).sum() / len(
                epoch_nn_intervals)

            total_contributions_d = np.sqrt(deceleration_index) * csi_cvi_features['cvi']
            total_contributions_a = np.sqrt(acceleration_index) * csi_cvi_features['csi']

            epoch_hrv_indices['Cd'] = total_contributions_d
            epoch_hrv_indices['Ca'] = total_contributions_a
            epoch_hrv_indices['SD2d'] = np.var(epoch_hrv_indices['Cd'])
            epoch_hrv_indices['SD2a'] = np.var(epoch_hrv_indices['Ca'])

            # calculate percentage of inflection points of RR intervals series
            rr_diff = np.diff(epoch_nn_intervals)
            num_inflection_points = ((rr_diff[1:] > 0) & (rr_diff[:-1] < 0)).sum()
            percentage_inflection_points = num_inflection_points / len(epoch_nn_intervals)
            epoch_hrv_indices['PIP'] = percentage_inflection_points

            # calculate MCVNN index
            median_abs_dev = np.median(np.abs(epoch_nn_intervals - np.median(epoch_nn_intervals)))
            median_abs_diff = np.median(np.abs(np.diff(epoch_nn_intervals)))
            mcvnn = median_abs_dev / median_abs_diff
            epoch_hrv_indices['MCVNN'] = mcvnn

            # Calculate DFA_alpha1
            dfa_alpha1 = nolds.dfa(epoch_nn_intervals, nvals=None, overlap=True, order=1, fit_trend="poly", fit_exp="RANSAC", debug_plot=False, debug_data=False, plot_file=None)
            epoch_hrv_indices['DFA_alpha1'] = dfa_alpha1

            sd2d = np.var(total_contributions_d)
            sd2a = np.var(total_contributions_a)
            epoch_hrv_indices['SD2d'] = sd2d
            epoch_hrv_indices['SD2a'] = sd2a
            epoch_hrv_indices['sdnn/cvnni'] = epoch_hrv_indices['sdnn'] / epoch_hrv_indices['cvnni']
            epoch_hrv_indices['user_email'] = email
            epoch_hrv_indices['epoch_index'] = i // step_intervals + 1
            hrv_indices.append(epoch_hrv_indices)

        except ValueError as e:
            print(f"Error calculating features for epoch {i}-{i+epoch_intervals}: {str(e)}")
            continue


    return pd.DataFrame(hrv_indices), pd.DataFrame(hr_values)

def main(email: str, date: str) -> None:
    """
    Main function which retrieves ECG data from a MongoDB database using the given email and date,
    processes and analyzes the ECG data using the defined functions, 
    saves the derived features to CSV files, 
    and saves the plots of the ECG signals with the R-peaks to .png files.

    Args:
    email (str): Email of the user
    date (str): Date of the ECG data in the format YYYY_MM_DD
    """
   
    DATABASE_URL = os.getenv('DATABASE')
    client = MongoClient(DATABASE_URL)
    db = client['cxe']  
    users_collection = db.ecg_signals  

    user_data = users_collection.find_one({"email": email})
    
    if user_data:
        key = 'ecg_signal_' + date
        if key in user_data:
            signal_data = np.array(user_data[key])
            
            out, rr_intervals_list, rr_intervals_without_outliers, interpolated_rr_intervals, nn_intervals_list, interpolated_nn_intervals = process_data(signal_data, sampling_rate=250.0)
            hrv_indices, hr_values = hrv_analysis(interpolated_nn_intervals=interpolated_nn_intervals, email=email)
            
            if os.path.exists("features"):
                hrv_indices.to_csv(f"features/hrv_indices_{email}_{date}.csv")
                hr_values.to_csv(f"features/hr_values_{email}_{date}.csv")
                
            else:
                os.makedirs("features")
                hrv_indices.to_csv(f"features/hrv_indices_{email}_{date}.csv")
                hr_values.to_csv(f"features/hr_values_{email}_{date}.csv")

            print(f"HRV indices and values for {email} on {date} saved.")

            plot_ecg_and_r_peaks(signal_data, out)
            
            if os.path.exists("ecg_rr_plots"):
                plot_filename = f'ecg_rr_plots/{email}_{date}.png'
                plt.savefig(plot_filename)
                plt.close()  
            else:
                os.makedirs("ecg_rr_plots")
                plot_filename = f'ecg_rr_plots/{email}_{date}.png'
                plt.savefig(plot_filename)
                plt.close() 

            print(f"ECG plot saved: {plot_filename}")
        else:
            print(f"No ECG data for {email} on {date}")
    else:
        print(f"No user found with email {email}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process email and date.')
    parser.add_argument('email', type=str, help='Email of the user')
    parser.add_argument('date', type=str, help='Date of the ECG data in the format YYYY_MM_DD')
    args = parser.parse_args()

    main(args.email, args.date)
