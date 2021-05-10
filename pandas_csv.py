import pyodbc as odbc
import pandas as pd

"""
Step 1. Importing dataset from CSV
"""
df = pd.read_csv(r'/home/blake/PycharmProjects/email-toolbox/customers.csv')

"""
Step 2. Specify columns we want to import
"""
columns = ['name', 'email', 'balance']

# df_data = df[columns]


"""
Step 3. Create SQL Server connection string
"""
DRIVER = 'mysql:'
SERVER_NAME = 'localhost'
DATABASE_NAME = 'customers_db'


def connection_string(driver, server_name, database_name):
    conn_string = f"""
        DRIVER={{{driver}}};
        SERVER={server_name};
        DATABASE={database_name};
        Trust_Connection=yes;
        username=root;
        password=HenryLikes2Bark!
    """
    return conn_string


"""
Step 4. Create database connection instance
"""
try:
    conn = odbc.connect(connection_string(DRIVER, SERVER_NAME, DATABASE_NAME))
except odbc.DatabaseError as e:
    print('Database Error:')
    print(str(e.value[1]))
except odbc.Error as e:
    print('Connection Error:')
    print(str(e.value[1]))