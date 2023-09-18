import Aidlab
import argparse
from Aidlab.Signal import Signal
from pymongo import MongoClient
from datetime import datetime
import os

class MainManager(Aidlab.Aidlab):
    """
    A class used to represent the main manager for the Aidlab device

    Attributes:
    client: MongoDB client
    email: The email of the user

    Methods:
    did_connect(aidlab): Method triggered when the Aidlab device is connected.
    did_disconnect(aidlab): Method triggered when the Aidlab device is disconnected.
    did_receive_ecg(aidlab, timestamp, values): Method triggered when the ECG signal is received from the Aidlab device.
    """

    def __init__(self, client, email):
        super().__init__()
        self.client = client
        self.email = email

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_ecg(self, aidlab, timestamp, values):
        db = self.client['cxe']  
        ecg_collection = db.ecg_signals 
        date = datetime.now().strftime("%Y_%m_%d")
        ecg_field = f"ecg_signal_{date}"
        ecg_collection.update_one({"email": self.email}, {"$push": {ecg_field: {"$each": values}}}, upsert=True)
                
if __name__ == '__main__':
 
    parser = argparse.ArgumentParser(description='Process email.')
    parser.add_argument('email', type=str, help='Email of the user')
    args = parser.parse_args()
    DATABASE_URL = os.getenv('DATABASE')
    client = MongoClient(DATABASE_URL)
    signals = [Signal.ecg]
    main_manager = MainManager(client, args.email)
    main_manager.connect(signals)

    while True:
        pass
