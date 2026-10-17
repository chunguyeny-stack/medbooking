import os
import pymssql
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Kết nối SQL Server bằng pymssql."""
    conn = pymssql.connect(
        server=os.getenv('DB_SERVER', 'localhost'),
        port=int(os.getenv('DB_PORT', '1433')),
        user=os.getenv('DB_USER', 'sa'),
        password=os.getenv('DB_PASSWORD', 'MedPassword123!'),
        database=os.getenv('DB_NAME', 'PhongKhamDB'),
        charset='UTF-8',
        as_dict=True
    )
    return conn