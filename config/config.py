# config.py
import os
from dotenv import load_dotenv



load_dotenv()


MONGO_DB_URL = os.getenv("MONGO_DB_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
