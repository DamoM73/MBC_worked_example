import sqlite3
import csv

def create_database():
    # connect to the databse and establish the cursor
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    
    # create the Postcode table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Postcode(
            code_id INTEGER PRIMARY KEY AUTOINCREMENT,
            postcode TEXT NOT NULL
        )        
        """
    )
    
    conn.commit()
    
    
    # create the Rewables table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Renewables(
            year_id INTEGER NOT NULL,
            code_id INTEGER NOT NULL,
            units INTEGER NOT NULL,
            output REAL,
            PRIMARY KEY (year_id,code_id),
            FOREIGN KEY (code_id) REFERENCES Postcode(code_id)
        )
        """
    )
    conn.commit()
    
    # create Suburb table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Suburb(
            suburb_id INTEGER PRIMARY KEY AUTOINCREMENT,
            code_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (code_id) REFERENCES Postcode(code_id)
        )
        """
    )
    conn.commit()


def populate_db(data_file):
    """
    Opens provided data_file and adds it to the database
    """
    
    with open(data_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        
        for row in csv_reader:
            # finding the columns of required data
            if row[0] == "Small Unit Installation Postcode":
                prev_rating_index = -1
                
                for index, col in enumerate(row):
                    if col == "Small Unit Installation Postcode":
                        postcode_index = index
                    elif col.endswith("Quantity"):
                        prev_units_index = index
                    elif col.endswith("kW"):
                        prev_rating_index = index
                    elif col.endswith("Quantity Total"):
                        units_index = index
                    elif col.endswith("kW Total"):
                        rating_index = index
            if  
                    
                        
    
# ----- CONSTANTS ----- #
DATA_SHEETS = [
    "data/2012_Postcode data for small-scale installations_SGU-Solar.csv",
    "data/2013_Postcode data for small-scale installations_SGU-Solar.csv",
    "data/2014_Postcode data for small-scale installations_SGU-Solar.csv",
    "data/2015_Postcode data for small-scale installations_SGU-Solar.csv",
    "data/2016_Postcode data for small-scale installations_SGU-Solar.csv",
    "data/2017_data for small-scale installations_SGU-Solar.csv",
    "data/2018_Postcode data for small-scale installations_all data.csv",
    "data/2019_Postcode data for small-scale installations_all data.csv",
    "data/2020_Postcode data for small-scale installations_all data.csv",
    "data/2021_2022_Postcode data for small-scale installations_SGU-Solar.csv"
]

DATABASE = "renewable_power.db"

# ---- MAIN PROGRAM ----

#create_database()

for data_sheet in DATA_SHEETS:
    populate_db(data_sheet)