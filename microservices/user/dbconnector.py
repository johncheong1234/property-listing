import mysql.connector

#DB Credentials
db_host = "localhost"
db_port = "3306"
db_user = "root"
db_password = ""
db_database = "SGP_User"

#Tables
tables = dict()
tables["User"] = """
    CREATE TABLE User (
        userId int auto_increment unique not null,
        username varchar(100) not null,
        name varchar(50) not null,
        password varchar (100) not null,
        email varchar(100) unique not null,
        nric varchar(50) not null,
        apiKey varchar(50) null,
        description varchar(100) null,
        PRIMARY KEY(userId)
    );
"""

#Dummy Data 
dummy_data = dict()
dummy_data["User"] = """
    INSERT INTO User(username, name, password, email, nric)
    VALUES
    ('john', 'John Cheong', 'abc', 'john@gmail.com', 'S9720715H'),
    ('cynthia', 'Cynthia Yap', 'abc', 'cynthia@gmail.com', 'S9162408E'),
    ('jiafang', 'Wu Jiafang', 'abc', 'jiafang@gmail.com', 'S9176434W'),
    ('huiwen', 'Tay Hui Wen', 'abc', 'huiwen@gmail.com', 'S9314686R'),
    ('xq', 'Lin Xiong Qing', 'abc', 'xiongqing@gmail.com', 'S9812381D'),
    ('robin', 'Robin Chong', 'abc', 'robin@gmail.com', 'S7079468O'),
    ('joshua', 'Joshua Wong', 'abc', 'joshua@gmail.com', 'S9394408S'),
    ('lingjia', 'Ow Ling Jia', 'abc', 'lingjia@gmail.com', 'S9933002D'),
    ('jiewwei', 'Lim Jiew Wei', 'abc', 'jiewwei@gmail.com', 'S9280983F'),
    ('xiyang', 'Lim Xi Yang', 'abc', 'xiyang@gmail.com', 'S8098908J'),
    ('eugene', 'Loo Eu Gene', 'abc', 'eugene@gmail.com', 'S7004666K'),
    ('xianjian', 'Han XingJian', 'abc', 'xingjian@gmail.com', 'S7575393L'),
    ('jowann', 'Yeak Jo Wann', 'abc', 'jowann@gmail.com', 'S8723682X'),
    ('jane', 'Jane', 'abc', 'jane@gmail.com', 'S7922006B'),
    ('liangsen', 'Liang Sen', 'abc', 'liangsen@gmail.com', 'S9399901M'),
    ('paulgriffin', 'Paul Griffin', 'abc', 'paulgriffin@gmail.com', 'S8286147Q'),
    ('swetha', 'Swetha', 'abc', 'swetha@gmail.com', 'S8155758Y'),
    ('lingxiao', 'Jiang Ling Xiao', 'abc', 'lingxiao@gmail.com', 'S9289691U'),
    ('swapna', 'Swapna', 'abc', 'swapna@gmail.com', 'S8743575I'),
    ('jongin', 'Kim Jong In', 'abc', 'jongin@gmail.com', 'S7281474O'),
    ('soohyun', 'Kim Soo Hyun', 'abc', 'soohyun@gmail.com', 'S9086786P'),
    ('suzy', 'Bae Suzy', 'abc', 'suzy@gmail.com', 'S8033030A'),
    ('benjamin', 'Benjamin Gan', 'abc', 'benjamin@gmail.com', 'S8392527C'),
    ('kinmeng', 'Tan Kin Meng', 'abc', 'kinmeng@gmail.com', 'S8552344G');
"""

#================= EXECUTION Examples =================
# select_one("SELECT * FROM Property")
# select_all("SELECT * FROM Property")
# select_one_params("SELECT * FROM Property WHERE propertyId = %s", (1,))
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

def select_one_params(query, params):
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


