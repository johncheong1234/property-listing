import mysql.connector

#DB Credentials
db_host = "localhost"
db_port = "3306"
db_user = "root"
db_password = ""
db_database = "SGP_Auction"

#Tables
tables = dict()
tables["Auction"] = """
    CREATE TABLE Auction(
        auctionId int auto_increment unique not null, 
        startDate datetime not null,
        endDate datetime not null,
        closed int DEFAULT 0,
        dateCreated datetime not null,
        propertyId int not null, 
        PRIMARY KEY (auctionId));
    """

tables["Bid"] = """
    CREATE TABLE Bid(
        bidId int auto_increment unique not null, 
        amount float not null,
        userId int not null, 
        auctionId int not null, 
        dateCreated datetime not null,
        PRIMARY KEY (bidId));
"""

#Dummy Data 
dummy_data = dict()
dummy_data["Auction"] = """
    INSERT INTO Auction(startDate, endDate, dateCreated, propertyId)
        VALUES
        ('2021-03-15', '2021-05-15', '2021-03-15', 1), 
        ('2021-03-15', '2021-05-15', '2021-03-15', 2)
"""

#================= EXECUTION Examples =================
# select_one("SELECT * FROM Property")
# select_all("SELECT * FROM Property")
# select_one_parameters("SELECT * FROM Property WHERE propertyId = %s", (1,))
# select_all_parameters("SELECT * FROM Property WHERE propertyType = %s", ("HDB",))
# execute("INSERT INTO Property(...) VALUES(...)")
# execute_parameters("INSERT INTO Property(title, type) VALUES (%s, %s)", ("Bedok", "HDB"))

#================= *** DO NOT TOUCH *** =================
def checkDBRequirements(tables):
    conn = mysql.connector.connect(
        host=db_host,
        port= db_port,
        user= db_user,
        password=db_password
    )
    if(hasDatabase(conn, db_database)):
        mycursor = conn.cursor()
        mycursor.execute("USE " + db_database)
        
        if hasTables(conn, tables) == True:
            return True

    return False

# Database Setup
def hasDatabase(conn, database):
    if _hasDatabase(conn, database) == False:
        #Database not found, attempt to create
        print("Database not found, attempt to create...")
        mycursor = conn.cursor()
        mycursor.execute("CREATE DATABASE " + database)

    if _hasDatabase(conn, database):
        print("DATABASE: " + database + " (ACTIVE)")
        return True
    return False
    
def _hasDatabase(conn, database):
    #Try to obtain databse
    mycursor = conn.cursor()

    mycursor.execute("SHOW DATABASES")
    result = mycursor.fetchall()

    for db in result:
        if(database.lower() == db[0].lower()):
            return True
    return False

# Tables
def hasTables(conn, tables):
    for table in tables:
        createTable = _hasTable(conn, table) == False
        if createTable:
            #Database not found, attempt to create
            print("Table not found, attempt to create...")
            mycursor = conn.cursor()
            query = tables[table]
            
            mycursor.execute(query)

        if _hasTable(conn, table):
            if createTable == True:
                if table in dummy_data.keys():
                    print("Loading dummy data for " + table)
                    _loadDummyData(conn, dummy_data[table])
                
            print("TABLE: " + table + " (ACTIVE)")
        else:
            print("An error has occurred, unable to create TABLE: " + table)
            return False
    return True

def _hasTable(conn, table):
    #Try to obtain table
    mycursor = conn.cursor()

    mycursor.execute("SHOW TABLES")
    result = mycursor.fetchall()

    for t in result:
        if(table.lower() == t[0].lower()):
            return True
    return False

def _loadDummyData(conn, dummyData):
    mycursor = conn.cursor()
    try:
        mycursor.execute(dummyData)
        conn.commit()
    except Exception as e:
        print(f"Error unable to load dummy data: ({str(e)})")

# Get cursor
setup_successful = checkDBRequirements(tables)
def getDBConnection():
    if(setup_successful == True):
        conn = mysql.connector.connect(
            host=db_host,
            port= db_port,
            user= db_user,
            password=db_password,
            database=db_database
        )
        return conn
    return None

#Functions
def select_one(query):
    try:
        conn = getDBConnection()
        if conn != None:
            cursor = conn.cursor()
            cursor.execute(query)

            result = cursor.fetchone()
            if result != None:
                columns = cursor.description 
                return {columns[index][0]:column for index, column in enumerate(result)}
    except Exception as e:
        print(f"DB Error occurred ({db_database}): {str(e)}")
        return None
    return None

def select_one_parameters(query, params):
    try:
        conn = getDBConnection()
        if conn != None:
            cursor = conn.cursor()
            cursor.execute(query, params)

            result = cursor.fetchone()
            if result != None:
                columns = cursor.description 
                return {columns[index][0]:column for index, column in enumerate(result)}
    except Exception as e:
        print(f"DB Error occurred ({db_database}): {str(e)}")
        return None
    return None

def select_all(query):
    try:
        conn = getDBConnection()
        if conn != None:
            cursor = conn.cursor()
            cursor.execute(query)

            columns = cursor.description 
            return [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    except Exception as e:
        print(f"DB Error occurred ({db_database}): {str(e)}")
        return None
    return None

def select_all_parameters(query, params):
    try:
        conn = getDBConnection()
        if conn != None:
            cursor = conn.cursor()
            cursor.execute(query, params)

            columns = cursor.description 
            return [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    except Exception as e:
        print(f"DB Error occurred ({db_database}): {str(e)}")
        return None
    return None
    
def execute(query):
    try:
        conn = getDBConnection()
        if conn != None:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return True
    except Exception as e:
        print(f"DB Error occurred ({db_database}): {str(e)}")
        return False
    return False

def execute_parameters(query, params):
    try:
        conn = getDBConnection()
        if conn != None:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
    except Exception as e:
        print(f"DB Error occurred ({db_database}): {str(e)}")
        return False
    return False

def insert(query):
    try:
        conn = getDBConnection()
        if conn != None:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

            cursor.execute('SELECT last_insert_id()')
            result = cursor.fetchone()
            if result != None:
                return result[0]
    except Exception as e:
        print(f"DB Error occurred ({db_database}): {str(e)}")
        return None
    return None

def insert_parameters(query, params):
    try:
        conn = getDBConnection()
        if conn != None:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            cursor.execute('SELECT last_insert_id()')
            result = cursor.fetchone()
            if result != None:
                return result[0]
    except Exception as e:
        print(f"DB Error occurred ({db_database}): {str(e)}")
        return None
    return None


