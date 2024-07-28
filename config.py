import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host = os.getenv('host'),
    user = os.getenv('user'),
    password = os.getenv('password'),
    database = os.getenv('database'),
    # port = int(os.getenv('port'))
)

cursor = conn.cursor()