import argparse
from pymongo import MongoClient
import os

def fetch_records(email):
    """
    Fetch ECG records from MongoDB for a given user's email.

    Args:
    email (str): The email of the user.

    Returns:
    None. This function prints the keys of records in the console.
    """
    DATABASE_URL = os.getenv('DATABASE')
    client = MongoClient(DATABASE_URL)
    db = client['cxe']  
    ecg_collection = db.ecg_signals 

    user_ecg_records = ecg_collection.find({"email": email})
    for record in user_ecg_records:
        print(list(filter(lambda key: key.startswith('ecg_signal_'), record.keys())))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch ECG records.')
    parser.add_argument('email', type=str, help='Email of the user')
    args = parser.parse_args()
    fetch_records(args.email)
