from src.connections.mongodb_connections import MongoDBConnection
import logging
import pandas as pd
from config.constant import Input_data_path
import os

logging.basicConfig(
    level=logging.DEBUG,
    format="%a(asctime)s - %(levelname)s - %(message)s"

)

def data_ingestion():
    try:
        # getting tyhe collection and loading the data
        data_connector = MongoDBConnection()
        collection = data_connector.get_collection()
        df = pd.DataFrame(list(collection.find({})))

        if "_id" in df.columns:
            df = df.drop("_id", axis=1)
        logging.info(f"data has been successfully loaded...")
        df = df[df["CustomerID"] != "C2867825"]
        print(df.head())
        #os.makedirs(Input_data_path, exist_ok=True)
        df.to_csv(Input_data_path)
        return df
    
    except Exception as e:
        logging.error(f"error occurred while loading the dataset from the database {e}")
        return None

