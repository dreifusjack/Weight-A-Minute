# Weight-a-Minute: Fitness Database System

Welcome to **Weight-a-Minute**, our comprehensive MySQL-based database system designed to support a full-featured fitness platform. 
This project includes schema creation and automated CSV data ingestion using Python and SQLAlchemy.

## Database File Structure

```bash
├── db_csvs/                    # Folder containing all CSV files for data insertion
├── 01_WeightAMinute DDL.sql    # SQL script to initialize database and schema
├── 02_insert_data.py           # Python script to load CSVs into the database
└── README.md                   # This file
```

## Project Steps
### Step 1
#### Implementing the Database with SQL
Before we added mock data to our fitness database, we needed a fully structured, relational schema to work with. This is where we used our  01_WeightAMinute DDL.sql file.
This comprehensive SQL script served as the blueprint for our entire database. It performed the following key operations:
- Dropped any existing version of the weightaminute database to ensure a clean slate
- Created a fresh database named weightaminute
- Defined all 17 interrelated tables

Using DataGrip, we executed the entire DDL file in one go by opening the SQL console connected to our MySQL instance, pasting the script, and running it. DataGrip's schema visualization tools made it easy to confirm that all the relationships were properly mapped, with no missing references or structural issues.

This step was critical for us because it guaranteed consistency across different development environments and ensured our data import process would not encounter issues due to missing tables or invalid constraints. 

### Step 2
#### Creating Mock Data with Mockaroo
To simulate realistic data for our fitness platform, we leveraged Mockaroo as our choice for data generation. This allowed us to prototype and build our database schema with varied and coherent sample data before implementing any frontend or backend functionality.

We crafted 17 unique tables to reflect the complexity and depth of a real-world fitness platform. These tables include entities such as Users, Workouts, Exercises, Trainers, Gyms, Records, BlogPosts, and others; each representing a critical system component. For each table, we carefully selected the appropriate data types, formats, and constraints to ensure integrity and relational consistency.

Mockaroo’s flexibility allowed us to define custom fields and relationships to mimic real-world patterns (e.g. email formats and timestamps). For instance, we generated workout durations that aligned realistically with workout types, and matched exercises appropriately with muscle groups in our Exercises table.

Additionally, we used Mockaroo’s data preview and downloadable CSV features to quickly iterate and refine our datasets. This saved us significant time and ensured our sample data helped uncover edge cases or improvements needed in the schema early on.

Ultimately, this step laid a solid foundation for testing queries, validating relationships, and developing robust insertion scripts, all while providing a realistic dataset to explore the system's functionality end-to-end.

### Step 3
#### Inserting Mock Data into the Database with Python
Once we made our database with Mockaroo, the next step was to bring our mock data to life by uploading it into a working MySQL database. We used our file 02_insert_data.py, which automates the process of importing data from CSV files into a MySQL database, without the need to manually write INSERT SQL statements.

The script uses the dotenv package to securely load database credentials and connection information (user, password, host, port, and database name) from a .env file. This allows for clean and secure configuration management. We also implemented a retry mechanism is implemented in the create_db_connection() function to handle cases where the MySQL container might not be ready immediately. It attempts to connect multiple times with delays in between, printing helpful logs for debugging.

Each CSV file is read into a pandas DataFrame, and its contents are inserted into a MySQL table. The table name is automatically derived from the CSV filename, and the data is inserted using SQLAlchemy’s to_sql() method. Existing tables with the same name are replaced. By running this script as part of the container initialization, all CSV files in the directory can be quickly and reliably loaded into the database every time the environment is spun up.
