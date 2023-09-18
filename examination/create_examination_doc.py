import argparse
from pymongo import MongoClient
import os
import pandas as pd

def fetch_records(email):
    """
    Fetches user and emotion images records from MongoDB and writes them to a CSV file.

    This function takes a user's email as input, then retrieves the corresponding user's details
    and emotion images records from a MongoDB database. It creates a DataFrame from the records,
    merges the user's details into the DataFrame, and writes the result to a CSV file.

    Args:
        email: The email of the user whose records are to be fetched.
    """
    DATABASE_URL = os.getenv('DATABASE')
    if DATABASE_URL is None:
        print("No DATABASE environment variable set.")
        return

    client = MongoClient(DATABASE_URL)
    db = client['cxe']

    users_collection = db.users
    user_data = users_collection.find_one({"email": email}, {'_id': 0, 'password': 0, '__v': 0})
    if user_data is None:
        print(f"No user found for email {email} in users collection.")
        return

    emotionsimages_collection = db.emotionsimages
    emotionsimages_records = list(emotionsimages_collection.find({"user": email}, {'_id': 0}))

    if len(emotionsimages_records) == 0:
        print(f"No records found for email {email} in emotionsimages collection.")
        return

    records_df_list = []
    for record in emotionsimages_records:
        emotions_df = pd.DataFrame(record['emotions'])
        emotions_df['user'] = record['user']
        emotions_df['image'] = record['image']
        records_df_list.append(emotions_df)

    records_df = pd.concat(records_df_list, ignore_index=True)

    user_data_df = pd.DataFrame([user_data])

    merged_df = pd.merge(records_df, user_data_df, left_on='user', right_on='email')
    merged_df.to_csv(f"examination_raw/examination_{email}.csv", index=True, index_label='index')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch emotionsimages records.')
    parser.add_argument('email', type=str, help='Email of the user')
    args = parser.parse_args()
    if args.email:
        print(f"Fetching records for email {args.email}.")
        fetch_records(args.email)
    else:
        print("No email provided.")
