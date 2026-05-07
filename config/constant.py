import os
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#Mongodb Configuration
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE = "Apex_trust_customer_transactions"
MONGO_COLLECTION = "Apex_Customer"


Input_data_path = os.path.join(BASE_DIR, "Dataset", "Apex_Trust_Customer_Data.csv")