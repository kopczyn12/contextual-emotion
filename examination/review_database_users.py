import argparse
from pymongo import MongoClient
import os
import pprint

def fetch_records(email):
    """
    Fetches the records of a user from the 'users' collection in the database.

    This function connects to a MongoDB database, retrieves all records from the 
    'users' collection that correspond to a specified user, excluding 'password', 
    '_id' and '__v' fields, and then prints these records.

    Args:
        email: The email of the user for which to fetch records.
    """
    
    DATABASE_URL = os.getenv('DATABASE')
    if DATABASE_URL is None:
        print("No DATABASE environment variable set.")
        return

    client = MongoClient(DATABASE_URL)
    db = client['cxe']

    users_collection = db.users
    user_records = users_collection.find({"email": email}, {"password": 0, "_id": 0, "__v": 0})  # Exclude 'password', '_id' and '__v' fields
    for record in user_records:
        pprint.pprint(record)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch user records.')
    parser.add_argument('email', type=str, help='Email of the user')
    args = parser.parse_args()
    if args.email:
        print(f"Fetching records for email {args.email}.")
        fetch_records(args.email)
    else:
        print("No email provided.")
