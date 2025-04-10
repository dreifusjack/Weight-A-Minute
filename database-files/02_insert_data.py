"""
File: insert_data.py
Author: Owen Sharpe
Description: Inserting data from CSV files into the database using Python packages, rather than INSERT SQL statements.
"""

# import libraries
import os
import time
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


# add connection retry logic
def create_db_connection(max_retries=5, retry_delay=3):

    # load the env file
    load_dotenv()

    # get .env credentials
    user = os.getenv("DB_USER")
    password = os.getenv("MYSQL_ROOT_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")
    print(f"Attempting to connect to database {db} at {host}:{port}")

    # try to connect with retries
    for attempt in range(max_retries):
        try:
            connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
            print(f"Connecting with: mysql+pymysql://{user}:****@{host}:{port}/{db}")
            engine = create_engine(connection_string)

            # test the connection
            with engine.connect() as conn:
                pass
            print("Database connection successful!")
            return engine
        except Exception as e:
            print(f"Connection attempt {attempt+1}/{max_retries} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to the database.")
                raise


# main execution
def main():
    try:

        # check if folder exists
        folder = '/app/db_csvs'
        if not os.path.exists(folder):
            print(f"Warning: Folder {folder} does not exist.")

            # try other path
            folder = '/database-files/db_csvs'
            if not os.path.exists(folder):
                print(f"Warning: Alternative folder {folder} does not exist either.")

                # list available directories for debugging
                print("Available directories in /docker-entrypoint-initdb.d/:")
                if os.path.exists('/docker-entrypoint-initdb.d/'):
                    print(os.listdir('/docker-entrypoint-initdb.d/'))
                return

        # gather csv files
        csv_files = [file for file in os.listdir(folder) if file.endswith('csv')]

        if not csv_files:
            print(f"No CSV files found in {folder}")
            return

        print(f"Found {len(csv_files)} CSV files: {csv_files}")

        # create database connection
        engine = create_db_connection()

        # insert CSVs into table
        for file in csv_files:
            file_path = os.path.join(folder, file)
            print(f"Reading file: {file_path}")
            df = pd.read_csv(file_path)

            # use filename as the table name
            table_name = os.path.splitext(file)[0]

            print(f"Inserting {len(df)} rows into table {table_name}")
            df.to_sql(table_name, con=engine, index=False, if_exists='replace')
            print(f'Successfully inserted {file} into table {table_name}')

    except Exception as e:
        print(f"Error in main execution: {str(e)}")


if __name__ == "__main__":

    # wait to ensure MySQL is fully initialized
    print("Waiting for database to be ready...")
    time.sleep(5)
    main()
