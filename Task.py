# Import from the Library
import sqlite3
from datetime import datetime
import os
import os.path
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ask the user which file they want to use.
while True:
    in_file = input("\nPlease enter the filename: ")
    try:
        f = open(in_file, "r")
    except FileNotFoundError:
            if os.path.isfile(in_file) and os.access(in_file, os.R_OK):
                print("File exists and is readable")
            elif '.' not in in_file:
                print("File does not contains extensions")
            elif in_file[-4:-3] != ".":
                print("File extensions is not valid")
            else:
                print("Either the file is missing or not readable.")
    else:
        break 
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Search the year in the file
with open(in_file, 'r') as fp:
    lines = fp.readlines()
    for row in lines:   # The program checks the rows until it finds the Year so it can save the year to the variable.
        word = 'Years='
        if row.find(word) != -1:
            values_start_line = lines.index(row)+4  
            yl = lines[lines.index(row)]
            first_a = yl.index('=')
            a_split = yl[first_a:].split('=')
            a_split[0] = yl[:first_a] + a_split[0]
            a_split = [x.strip() for x in a_split]
            year = a_split[2][:4]
            year = int(year)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Connect to the database and create it. If this exists already the program sends a message about it and stops.
conn = sqlite3.connect("data_trans.db")
c = conn.cursor()
try:
    c.execute("CREATE TABLE python_datas (Xref INTEGER, Yref INTEGER, Date DATE, Value INTEGER)")
except sqlite3.OperationalError:
    print("The database already exists.")
    exit()
print("Table created!")
conn.close()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Read out the data from the file
with open(in_file, 'r') as fp:
    lines = fp.readlines() # read all lines using readline()
    count = 1
    z = 0
    j = 1  #count the months
    Xref = 0
    Yref = 0
    countgrid = 1
    for row in lines:
            word = 'Grid-ref='
            if row.find(word) != -1:
                countgrid = countgrid+1
                yl = lines[lines.index(row)]
                first_a = yl.index('=')
                a_split = yl[first_a:].split('=')
                a_split[0] = yl[:first_a] + a_split[0]
                a_split = [x.strip() for x in a_split]
                Xref = a_split[1].split(', ')
                Xref = int(Xref[0])                     # Get the Xref data
                a_split = yl[first_a:].split(', ')
                Yref = a_split[1].replace('\n', '')
                Yref = int(Yref)                        # Get the Yref data
                count = count + 1
            
            else:
                if lines.index(row) > 4:
                    val = row.split()
                    months = 1
                    day = 1
                    z = 0       # variable for value
                    for y in val:
                        days = str(day)
                        monthss = str(months)
                        years = str(year) 
                        str_date = str(months)+days+str(years)
                        date = datetime.strptime(str_date, '%m%d%Y').strftime('X%d/X%m/%Y').replace('X0','X').replace('X','')
                        val = row.split()
                        # ------------------------------------------------------------------------------------------------------------------------------------------------------------                        
                        # Write the data on the screen and into the db.
                        print("Data: ", Xref, Yref, date, val[z])
                        print("Data inserted!")
                        conn = sqlite3.connect("data_trans.db")    # Connect to the database
                        c = conn.cursor()
                        c.execute('INSERT INTO python_datas values (?, ?, ?, ?)', (Xref, Yref, date, val[z])) # Set the new values
                        conn.commit()   # Commit changes
                        conn.close()    # Close the connection    
                        # ------------------------------------------------------------------------------------------------------------------------------------------------------------
                        # Get the next month, year etc.
                        z = z+1
                        j = j+1
                        months = months+1
                        if months == 13 and year != 2000:
                            year = year+1
                        elif months == 13 and year == 2000:
                            year = 1991