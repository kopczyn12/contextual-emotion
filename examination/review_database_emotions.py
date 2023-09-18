import argparse
from pymongo import MongoClient
import os
import pprint

def fetch_records(email):

    """
    Fetches the records of a user from the 'emotionsimages' collection in the database.

    This function connects to a MongoDB database, retrieves all records from the 
    'emotionsimages' collection that correspond to a specified user, and prints 
    the records. 

    Args:
        email: The email of the user for which to fetch records.
    """
    
    DATABASE_URL = os.getenv('DATABASE')
    if DATABASE_URL is None:
        print("No DATABASE environment variable set.")
        return

    client = MongoClient(DATABASE_URL)
    db = client['cxe']

    emotionsimages_collection = db.emotionsimages
    user_records = list(emotionsimages_collection.find({"user": email}))  

    if len(user_records) == 0:
        print(f"No records found for email {email} in emotionsimages collection.")
    else:
        print(f"Found {len(user_records)} records for email {email} in emotionsimages collection:")
        for record in user_records:
            print(f"User: {record.get('user')}")
            print(f"Image: {record.get('image')}")
            print(f"_id: {record.get('_id')}")
            print(f"Emotions: {record.get('emotions')}")
            print("--------------------------------------------------------")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch emotionsimages records.')
    parser.add_argument('email', type=str, help='Email of the user')
    args = parser.parse_args()
    if args.email:
        print(f"Fetching records for email {args.email}.")
        fetch_records(args.email)
    else:
        print("No email provided.")
