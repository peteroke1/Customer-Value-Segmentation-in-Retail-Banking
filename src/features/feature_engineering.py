import pandas as pd
import numpy as np
from datetime import datetime
import logging

from src.data.data_ingestion import data_ingestion
from src.data.data_validation import data_validation

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class feature_eng:
    def calculate_rfm_metrics(data: pd.DataFrame):
        try:
            reference_date = data["TransactionDate"].max() + pd.Timedelta(days=1)
            print(f"Reference date for Recency calculation: {reference_date.date()}")

            # Calculate RFM metrics for each customer
            rfm_data = data.groupby("CustomerID").agg({
                "TransactionDate": lambda x: (reference_date - x.max()).days,
                "TransactionID": "count",
                "TransactionAmount": "sum"
            }).reset_index()

            rfm_data.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]
            logging.info("the rfm data has been successfully created:\n {rfm_data.head()}")
        
            customer_demography = data.groupby("CustomerID").agg({
                "CustomerDOB": "first",
                "CustGender": "first",
                "CustLocation": "first",
                "CustAccountBalance": "last"
            }).reset_index()
            logging.info(f"the customer demographic data has also been created {customer_demography.head()}")
            rfm_data = rfm_data.merge(customer_demography, on="CustomerID", how="left")
            logging.info(f"THe rfm_data has been successfully created:\n {rfm_data}")
            return rfm_data
        except Exception as e:
            logging.error(f"error occurred while calculating the rfm metrics and Data {e}")
    
    def calculating_rfm_scores(data: pd.DataFrame):
        try:
            data["R_Score"] = pd.qcut(data["Recency"], q=5, labels=[5,4,3,2,1])
            data["F_Score"] = pd.qcut(data["Frequency"], q=5, labels=[1,2,3,4,5])
            data["M_Score"] = pd.qcut(data["Monetary"], q=5, labels=[1,2,3,4,5])
            data[["R_Score", "F_Score", "M_Score"]] = data[["R_Score", "F_Score", "M_Score"]].astype(int)
            data["RFM_Score"] = data["R_Score"] + data["F_Score"] + data["M_Score"]
            logging.info("RFM score has successfully calculated...")
            logging.info(f"{data.head()}")
            return data
        except Exception as e:
            logging.error(f"error occurred while calculating the RFM scores... {e}")

customer_data = data_ingestion()
customer_data = data_validation(customer_data)
feature_engineering = feature_eng
customer_data = feature_engineering.calculate_rfm_metrics(customer_data)
customer_data = feature_engineering.calculating_rfm_scores(customer_data)