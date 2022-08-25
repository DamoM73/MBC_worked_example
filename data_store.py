import sqlite3

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
            year_id INTEGER,
            code_id INTEGER,
            units INTEGER,
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
            code_id INTEGER,
            name TEXT,
            FOREIGN KEY (code_id) REFERENCES Postcode(code_id)
        )
        """
    )
    conn.commit()
    
    
# ----- CONSTANTS ----- #
DATASHEETS = [
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

create_database()