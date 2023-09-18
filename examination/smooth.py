import pandas as pd

def merge_dataframe():
    """
    Merge two parts of the same DataFrame based on the nearest timestamp.

    This function reads a .csv file into a DataFrame, splits the DataFrame into two 
    DataFrames based on certain columns, sorts each DataFrame based on their respective 
    timestamp, and then merges them together using an asof join. The final merged 
    DataFrame is saved to a .csv file.
    """

    # Load the csv file into a DataFrame
    df = pd.read_csv('examination_merged/merged.csv')

    # Convert 'timestamp1' and 'timestamp2' to datetime format
    df['timestamp1'] = pd.to_datetime(df['timestamp1'], format='%d.%m.%Y, %H:%M:%S,%f')
    df['timestamp2'] = pd.to_datetime(df['timestamp2'], format='%d.%m.%Y, %H:%M:%S,%f')

    # Split the DataFrame into two DataFrames
    df1 = df[['Unnamed: 0', 'user', 'image', 'emotion','timestamp1','email','age','gender','occupation']].copy()
    df2 = df[['timestamp2', 'x', 'y']].copy()

    # Drop NaN values from 'timestamp1' column
    df1 = df1.dropna(subset=['timestamp1'])

    # Sort both DataFrames based on their respective timestamps
    df1 = df1.sort_values('timestamp1')
    df2 = df2.sort_values('timestamp2')

    # Merge the DataFrames based on nearest timestamp
    merged_df = pd.merge_asof(df1, df2, left_on='timestamp1', right_on='timestamp2', direction='nearest')

    # Save the merged DataFrame to a csv file
    merged_df.to_csv('merged_file_smooth_kuba30@gmail.csv', index=False)

# Execute the function
if __name__ == "__main__":
    merge_dataframe()
