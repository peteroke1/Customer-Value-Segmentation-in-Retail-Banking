import pandas as pd
import numpy as np
from src.data.data_ingestion import data_ingestion
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def data_validation(data: pd.DataFrame):
    try:
        customer_data = data.copy()
        duplicates = customer_data.duplicated().sum()
        logging.info(f"The total number of duplicates is {duplicates}")

        duplicate_transaction = customer_data["TransactionID"].duplicated().sum()
        logging.info(f"the total number of duplicated trasnsaction is {duplicate_transaction}")

        unique_customers = customer_data["CustomerID"].nunique()
        logging.info(f"the total number of unique value is {unique_customers}")

        gender_distribution = customer_data["CustGender"].value_counts()
        logging.info(f"the gender distribution is {gender_distribution}")

        missing_value = customer_data.isna().sum()
        logging.info(f"number of missing value is {missing_value}")

        customer_data = customer_data.dropna()
        logging.info("missing value is successfully dropped if there is any.")

        customer_data["TransactionDate"] = pd.to_datetime(customer_data["TransactionDate"], errors="coerce")
        logging.info("the transaction data has been successfully validated and the transaction date has been handled.")
        logging.info(f"the dataset info {customer_data.info()}")
        return customer_data
    except Exception as e:
        logging.error("error occur while validating the dataset {e}")

        


    
