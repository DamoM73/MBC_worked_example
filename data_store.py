import sqlite3
import csv

def create_database():
    
    print("Creating database")
    
    # connect to the databse and establish the cursor
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    
    # create the Postcode table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Postcode(
            postcode TEXT PRIMARY KEY,
            state TEXT NOT NULL
        )        
        """
    )
    
    conn.commit()
    
    
    # create the Rewables table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Installs(
            year INTEGER,
            postcode TEXT,
            units INTEGER,
            output REAL,
            PRIMARY KEY (year,postcode),
            FOREIGN KEY (postcode) REFERENCES Postcode(postcode)
        )
        """
    )
    
    conn.commit()
    
    # create Suburb table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Suburb(
            suburb_id INTEGER PRIMARY KEY AUTOINCREMENT,
            postcode TEXT NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (postcode) REFERENCES Postcode(postcode)
        )
        """
    )
    conn.commit()


def get_postcodes():
    """
    uses cursor to add postcodes from the postcode csv file
    cur: sqlite3 database cursor object
    """
    print("Processing postcodes")
    with open(POSTCODES) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        
        postcodes = []
        
        # read each row of the csv file
        for row in csv_reader:
            if row[0] != "postcode":
                postcode = row[0]
                suburb = row[1]
                state = row[3]
                if postcode not in postcodes:
                    add_postcode(postcode,state)
                    postcodes.append(postcode)
                add_suburb(postcode, suburb)



def add_postcode(postcode,state):
    # connect to the databse and establish the cursor
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    cur.execute(
        """
        INSERT INTO Postcode (postcode,state)
        VALUES (:postcode,:state)
        """,
        {
            "postcode":postcode,
            "state":state
        }
    )
    conn.commit()
            

def add_suburb(code_id, suburb):
    # connect to the databse and establish the cursor
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    cur.execute(
        """
        INSERT INTO Suburb (postcode, name)
        VALUES (:code_id, :suburb)
        """,
        {
            "code_id":code_id,
            "suburb":suburb
        }
    )
    conn.commit()    


def get_install_data(data_file):
    """
    Opens provided data_file and adds it to the database
    """
    
    print("Processing:",data_file)
    
    with open(data_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        
        # read each row of the csv file
        for index, row in enumerate(csv_reader):
            # values needed for database
            postcode = row[0]
            yr_1_total_units = 0
            yr_1_total_rating = 0
            yr_2_total_units = 0
            yr_2_total_rating = 0
            if index == 0:
                year_1 = int(row[3][4:8])
                if year_1 == 2021:
                    year_2 = 0
                else:
                    year_2 = int(row[27][4:8])
            elif index > 1:
                col_index = 3
                # get year 1 totals
                while col_index < 26:
                    yr_1_total_units += int(row[col_index])
                    col_index += 1
                    yr_1_total_rating += clean_rating(row[col_index])
                    col_index += 1
                # get year 2 totals
                if year_2 != 0:
                    while col_index < 51:
                        yr_2_total_units += int(row[col_index])
                        col_index += 1
                        yr_2_total_rating += clean_rating(row[col_index])
                        col_index += 1
            
                if postcode != "0":
                    add_install_data(year_1,postcode,yr_1_total_units,yr_1_total_rating)
                    if year_2 != 0:
                        add_install_data(year_2,postcode,yr_2_total_units,yr_2_total_rating)


def add_install_data(year,postcode,units,output):
    # connect to the databse and establish the cursor
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    cur.execute(
        """
        INSERT INTO Installs (year, postcode, units, output)
        VALUES (:year,:postcode,:units,:output)
        """,
        {
            "year":year,
            "postcode":postcode,
            "units":units,
            "output":output
        }
    )
    conn.commit()

                    
def clean_rating(rating):
    return float(rating.replace(",",""))

                
def populate_database():
        
    get_postcodes()
    
    for data_sheet in DATA_SHEETS:
        get_install_data(data_sheet)
    
        
                        
    
# ----- CONSTANTS ----- #
DATA_SHEETS = [
    "data/Postcode data for small-scale installations - SGU-Solar.csv",
    "data/Postcode data for small-scale installations 2012 - SGU-Solar.csv",
    "data/Postcode data for small-scale installations 2014 - SGU-Solar.csv",
    "data/Postcode data for small-scale installations 2016 - SGU-Solar.csv",
    "data/Postcode data for small-scale installations 2018 - SGU-Solar.csv",
    "data/Postcode data for small-scale installations 2020 - SGU - Solar.csv"
]

DATABASE = "renewable_power.db"

POSTCODES = "data/au_postcodes.csv"

# ---- MAIN PROGRAM ----

create_database()

populate_database()