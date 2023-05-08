
from dotenv import load_dotenv
import sys
import os
import mariadb

load_dotenv()  # load environment variables from .env file
db_host = os.getenv('DB_HOST')
db_port = int(os.getenv('DB_PORT')) 
db_database = os.getenv('DB_DATABASE')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

# Connect to MariaDB Platform

def connect():
    try: 
        conn = mariadb.connect( 
            host=db_host,
            port=db_port,
            database=db_database,
            user=db_username,
            password=db_password
        )

    except mariadb.Error as ex: 

        print(f"An error occurred while connecting to MariaDB: {ex}") 

        sys.exit(1) 


    # export DB connection to other files
    return conn
