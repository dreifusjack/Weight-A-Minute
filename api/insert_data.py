"""
File: insert_data.py
Author: Owen Sharpe
Description: Inserting data from CSV files into the database using Python packages, rather than INSERT SQL statements.
"""

# import libraries
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# gather csv files
folder = '"/apicode/db_csvs"'
csv_files = [file for file in os.listdir(folder) if file.endswith('csv')]

# load the env file
load_dotenv()

# get credentials
user = os.getenv("DB_USER")
password = os.getenv("MYSQL_ROOT_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

# create mySQL engine
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")

# insert CSVs into table
for file in csv_files:
    file_path = os.path.join(folder, file)
    df = pd.read_csv(file_path)

    # use filename as the table name
    table_name = os.path.splitext(file)[0]

    df.to_sql(table_name, con=engine, index=False, if_exists='replace')
    print(f'Inserted {file} into table {table_name}')