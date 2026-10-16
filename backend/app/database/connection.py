import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Kết nối SQL Server"""
    conn_str = (
        f"DRIVER={os.getenv('DB_DRIVER', 'ODBC Driver 18 for SQL Server')};"
        f"SERVER={os.getenv('DB_SERVER', 'localhost')};"
        f"DATABASE={os.getenv('DB_NAME', 'medbooking')};"
        f"UID={os.getenv('DB_USER', 'sa')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)