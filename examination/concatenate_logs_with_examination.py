import pandas as pd
from datetime import datetime, timedelta
import argparse

def append_logs(csv_path, txt_path, mail: str):
    """
    Appends logs from a txt file to a csv file based on nearest timestamps and then saves it as a new csv file.

    Args:
        csv_path (str): Path to the CSV file.
        txt_path (str): Path to the TXT file.
        mail (str): User's mail string which will be added in the filename of output file.
    """

    df_csv = pd.read_csv(csv_path)
    df_txt = pd.read_csv(txt_path, names=['timestamp1', 'x', 'y'])

    # Convert UNIX timestamp to datetime and then to the desired string format
    df_txt['timestamp1'] = pd.to_datetime(df_txt['timestamp1'], unit='s')
    df_txt['timestamp1'] = df_txt['timestamp1'] + timedelta(hours=1)
    df_txt['timestamp1'] = df_txt['timestamp1'].apply(lambda dt: dt.strftime('%d.%m.%Y, %H:%M:%S,%f')[:-3])  # Remove last 3 digits from microseconds

    df_csv = pd.concat([df_csv, df_txt], axis=1)
    df_csv['timestamp'] = pd.to_datetime(df_csv['timestamp'], format='%d.%m.%Y, %H:%M:%S,%f')
    df_csv['timestamp1'] = pd.to_datetime(df_csv['timestamp1'], format='%d.%m.%Y, %H:%M:%S,%f')

    df1 = df_csv[['index', 'user', 'image', 'emotion','timestamp','email','age','gender','occupation']].copy()
    df2 = df_csv[['timestamp1', 'x', 'y']].copy()

    df1 = df1.dropna(subset=['timestamp'])
    df1 = df1.sort_values('timestamp')
    df2 = df2.sort_values('timestamp1')

    merged_df = pd.merge_asof(df1, df2, left_on='timestamp', right_on='timestamp1', direction='nearest')
    merged_df.to_csv(f'examination_merged/merged{mail}.csv', index=False)

if __name__ == '__main__':
    """
    Main function to get inputs from the user to pass to append_logs function.
    """

    mail = input('Provide mail of user to concatenate: \n')
    parser = argparse.ArgumentParser(description='Append logs to CSV.')
    parser.add_argument('csv_path', type=str, help='Path to the CSV file')
    parser.add_argument('txt_path', type=str, help='Path to the TXT file')
    args = parser.parse_args()
    append_logs(args.csv_path, args.txt_path, mail)
