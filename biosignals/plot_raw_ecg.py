import argparse
import os
from pymongo import MongoClient
import matplotlib.pyplot as plt
from datetime import datetime

def main(email: str, date: str):
    """
    Retrieves and plots ECG data for a specific user and date.
    
    Args:
    email: The email of the user.
    date: The date of the ECG data in the format YYYY_MM_DD.
    
    Returns:
    None
    """
    
    DATABASE_URL = os.getenv('DATABASE')
    client = MongoClient(DATABASE_URL)
    db = client['cxe']  
    users_collection = db.ecg_signals  

    
    user_data = users_collection.find_one({"email": email})

    if user_data:
        key = 'ecg_signal_' + date
        if key in user_data:
            values = user_data[key]
            try:
                ecg_data = [float(value) * 1000 for value in values]
            except ValueError:
                print(f"Non-numeric data found in ECG data for {email} on {date}")
                return

            
            sampling_rate = 250  # Hz
            total_samples = len(ecg_data)
            time_seconds = [(i + 1) / sampling_rate for i in range(total_samples)]

            plt.figure(figsize=(25, 5))
            plt.plot(time_seconds, ecg_data)
            plt.title('ECG Signal')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Value (millivolts)')

            plt.xlim([0, time_seconds[-1]])

            
            plot_directory = 'ecg_raw_plots'
            os.makedirs(plot_directory, exist_ok=True)

            
            plot_filename = f'{plot_directory}/{email}_{date}.png'
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
