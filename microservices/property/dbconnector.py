import mysql.connector

#DB Credentials
db_host = "localhost"
db_port = "3306"
db_user = "root"
db_password = ""
db_database = "SGP_Property"

#Tables
tables = dict()
tables["Property"] = """
    CREATE TABLE Property(
        propertyId int auto_increment unique not null, 
        propertyType varchar (40), 
        title varchar(250) not null, 
        description varchar(1000) not null, 
        startingPrice int not null, 
        status varchar(10) not null, 
        termOfLease varchar(50) not null, 
        postalCode varchar(20) not null, 
        dateOfPurchase datetime not null,
        leaseCommencementDate datetime not null,
        sizeSQFT float not null,
        fullAddress varchar(200) not null, 
        displayPicture varchar(200) null,
        noOfRooms int not null,
        noOfToilets int not null, 
        dateCreated datetime not null,
        userId int not null, 
        PRIMARY KEY (propertyId));
    """

tables["PropertyImage"] = """
    CREATE TABLE PropertyImage (
        propertyImageId int auto_increment unique not null,
        propertyId int not null,
        path varchar(250) not null,
        PRIMARY KEY(propertyImageId)
    );
"""

#Dummy Data 
dummy_data = dict()
dummy_data["Property"] = """
    INSERT INTO Property(propertyId,propertyType, title, description, startingPrice, status, termOfLease, postalCode, dateOfPurchase, leaseCommencementDate,sizeSQFT,fullAddress, noOfRooms,noOfToilets,dateCreated,userId)
    VALUES
    (1,'Condominium', 'FLO Residence for Sale', ' Coral Edge LRT right at doorstep, walking distance to Punggol Plaza', 940000, 'Sold', '99', '828739', '2017-01-09', '2016-02-02', 1012, '1 Punggol Field Walk S828739', 3, 2, '2018-12-09', 1),
    (2,'Condominium', '1 Bed Condo for Sale in Hillion Residences', 'Mixed integrated development with mall, bus interchange, MRT & LRT right below the condo',788000, 'Available', '99', '677673', '2018-07-17', '2018-04-03', 441, 'Hillion Residences, 12 Jelebu Road S677673', 2, 1, '2019-07-07', 2),
    (3,'Executive Condo' , '3 Bed EC for Sale in La Casa' , 'North South Orientation , windy and bright unit',930000 , 'Available' , '99' , '737896' , '2010-10-18', '2008-11-07', 1185, 'Woodlands Drive 16 S737896' , 4 , 3 , '2017-10-01',2),
    (4,'HDB' , 'HDB Flat for Sale in 88 Dawson Road' , 'Walk to Dawson Place for amenities such as Foodcourt, 24 hr supermarket, bakery shoes, provision store, etc.',888000 , 'Available' , '99' , '142088' , '2017-10-12', '2016-12-06', 893 , '88 Dawson Road S142088' , 4 , 2 , '2018-10-03',3), 
    (5,'HDB' , 'HDB Flat for Sale in 674A Yishun Avenue 4' , 'Tastefully RENOVATED, Scandinavian Muji theme',499000 , 'Available' , '99' , '761674' , '2020-01-12', '2019-11-07', 1002 , '674A Yishun Avenue 4 S761674' , 3 , 2 , '2020-08-05',3), 
    (6,'Cluster House' , '4 Bed House for Sale in Le Royce @ Leith Park' , 'SMART home throughout the property', 2750000 , 'Available' , 'Freehold' , '547936' , '2020-04-27', '2018-09-08', 3499 , 'Leith Park, Leith Park S547936' , 5 , 4 , '2021-03-21',4), 
    (7,'Semi-Detached House' , '5 Bed House for Sale in 1B Asimont Lane' , 'Excellent internal layout with generous swimming pool and top-notch finishes',7800000 , 'Available' , 'Freehold' , '309939' , '2020-02-09', '2013-04-03', 2411 , '1B Asimont Lane, Asimont Lane S309939' , 6 , 6 , '2021-02-02',5), 
    (8,'Terraced House' , '5 Bed House for Sale in Victory Ville' , 'Facilities includes swimming pool, outdoor shower area, BBQ pits, children playground ',2300000 , 'Available' , 'Freehold' , '507904' , '2015-06-05', '2014-07-05', 3443 , 'Victory Ville, Toh Drive S507904' , 6 , 5 , '2017-05-05',5), 
    (9,'Bungalow' , '6 Bed House for Sale in Ponggol Park' , 'Tastefully renovated Detached House in District 19 Punggol with Balinese-Theme',5100000 , 'Sold' , '999' , '829482' , '2016-03-25', '2006-01-30', 4995 , 'Ponggol Park, Ponggol Twenty-Fourth Avenue S829482' , 7 , 6 , '2019-01-25',7), 
    (10,'Executive Condo' , '3 Bed EC for Sale in Riverparc Residence' , 'Gymnasium room and fitness corner, nearest bus stop is located at the Kadaloor Station which is only about 150 metres and 2 minutes of walking distance',1500000 , 'Sold' , '99' , '828800' , '2010-05-21', '2009-11-08', 2066 , 'Riverparc Residence, 102 Punggol Drive S828800' , 4 , 3 , '2019-02-21',7) , 
    (11,'Condominium' , '3 Bedder with Balcony' , 'Huge Balcony that can be used as dining area & Full Condo Facilities',1350000 , 'Sold' , '99' , '528588' , '2017-11-28', '2017-12-12', 1119 , '29 Tampines Street 86 S528588' , 4 , 2 , '2019-01-28',8), 
    (12,'HDB' , '3 Bed House for Sale in Woodlands', '3 min walk to 24 hours Sheng Siong Supermarket, coffeeshop, clinics, bakery and hair salon etc', 550000 , 'Available' , '99' , '738994' , '2018-07-26', '2017-10-20', 90 , '573C Woodlands Drive 16 S738994' , 4 , 2 , '2020-02-26',1), 
    (13,'HDB' , '3 Bed House for Sale in Compassvale Drive' , 'Amenities nearby: many eateries, supermarket & Compass One Shopping Centre - Approximately 5 mins walk to Sengkang MRT Station',599000 , 'Available' , '99' , '541217' , '2016-09-15', '2016-08-13', 92 , '217A Compassvale Drive S541217' , 3 , 2 , '2019-05-15',1), 
    (14,'HDB' , '4 Bedroom Premium Loft' , 'Sky gardens with lush landscaping are built on the upper floors, which offer communal spaces and breathtaking views.',1050000 , 'Sold' , '99' , '141092' , '2016-02-20', '2015-06-14', 95 , '93 Dawson Road S141092' , 4 , 2 , '2020-01-20',2), 
    (15,'Condominium' , 'Renovated 2 Bedroom House', 'Quiet, greenery and scenic  facing view/environment & walking distance to Bukit Timah Hill',1350000 , 'Available' , '999' , '588997' , '2011-07-18', '2011-10-10', 721 , '2 Jalan Anak Bukit S588997' , 3 , 2 , '2019-07-10',4), 
    (16,'HDB' , '3 Bed House for Sale in Buona Vista', 'Near to Star Vista & Holland Village (lots of good food) & walking distance from Buona Vista', 630000 , 'Sold' , '99' , '270026' , '2012-12-01', '2012-03-02', 67 , '26 Ghim Moh Link S270026' , 3 , 2 , '2020-01-01',5), 
    (17,'HDB' , 'High Floor House at Jalan Kayu' , '5 mins walk to many eateries and Seletar Mall Shopping Centre',388000 , 'Sold' , '99' , '791447' , '2013-04-14', '2012-04-07', 67 , '447A Jalan Kayu S791447' , 3 , 2 , '2018-04-12',6), 
    (18,'HDB' , '4 room unit Facing North East, bright and windy' , 'Kitchen equipped with Bosch appliances & Well Maintained Unit', 490000 , 'Available' , '99' , '673443' , '2015-11-11', '2015-04-05', 93 , '443C Fajar Road S673443' , 4 , 2 , '2017-11-01',7), 
    (19,'HDB' , '3 Bed House for Sale in Choa Chu Kang' , 'Near amenities such as coffeeshop, clinics, bakery, 24 hour supermarket and laundromat', 480000 , 'Sold' , '99' , '682812' , '2017-04-06', '2016-11-11', 93 , '812B Choa Chu Kang Avenue 7 S682812' , 4 , 2 , '2019-01-06',8), 
    (20,'Semi-Detached House' , 'Braddell Heights estate with koi pond, bamboo grove' , '4 large bedrooms including "granny" room on ground floor and ample space for study and work-from-home areas',4200000 , 'Sold' , 'Freehold' , '358683' , '2010-12-24', '2010-12-12', 3500 , 'Lynwood Grove S358683' , 5 , 3 , '2016-02-24',5), 
    (21,'HDB' , 'Spacious & unblocked view 5 room for sale' , 'Walking distance from Rivervale mall and Rivervale plaza & Bakau or Rumbia LRT stations',485000 , 'Available' , '99' , '542157' , '2001-04-04', '2001-03-22', 109 , '157B Rivervale Crescent S542157' , 5 , 2 , '2016-02-01',4), 
    (22,'HDB' , '5 room flat in Punggol' , '5 minutes walk to Punggol MRT & 5 mins walk to many eateries and Waterway Point Shopping Centre',498000 , 'Sold' , '99' , '820293' , '2002-04-01', '2001-06-25', 110 , '293 Punggol Central S820293' , 5 , 2 , '2016-01-01',3), 
    (23,'Condominium' , 'Spacious 3 bedroom apartment in Sembawang' , 'Approximately 1.2km to Yishun MRT and Northpoint City & near Eateries, supermarket, Chong Pang market ', 998000 , 'Available' , 'Freehold' , '758382' , '2000-05-23', '1998-04-11', 1377 , '369 Sembawang Road S758382' , 4 , 3 , '2018-02-23',2), 
    (24,'Condominium' , '2 Bedder in Sky Habitat with great view' , 'Near Bishan MRT, Junction 8 with unblocked view', 1218000 , 'Sold' , '99' , '573909' , '2015-01-19', '2015-01-07', 710 , '9 Bishan Street 15 S573909' , 3 , 1 , '2020-01-07',3), 
    (25,'Condominium' , 'Estuary 4 bedroom with garden resort view' , 'Pool and garden resort view & 10 min walk to Khatib MRT',1528000 , 'Available' , '99' , '769136' , '2013-05-20', '2013-04-04', 1528 , '93 Yishun Avenue 1 S769136' , 5 , 3 , '2017-03-11',5), 
    (26,'Condominium' , 'ForestVille @ Woodlands' , 'Easily connected to Vista Point,24 hrs Sheng Siong,childcare centres,parks & expressways', 1200000 , 'Available' , '99' , '737881' , '2017-05-04', '2016-05-17', 1247 , '24 Woodlands Drive 16 S737881' , 5 , 3 , '2019-04-14',6), 
    (27,'Condominium' , 'The Rivervale - 3 bedrooms for Sale!' , '10 mins to Buangkok MRT and near many amenities',988000 , 'Available' , '99' , '545125' , '2001-12-11', '2001-11-13', 1314 , '7 Rivervale Link S545125' , 4 , 2 , '2016-10-11',2), 
    (28,'Condominium' , 'Hertford Collection - 2 bedrooms for Sale!' , ' Mins away from Novena Square, Velocity @ Novena and City Square Mall & Private access to lap pool', 1660000 , 'Available' , 'Freehold' , '210050' , '2013-11-09', '2013-08-19', 1432 , '40 Hertford Road S210050' , 3 , 2 , '2018-01-02',1), 
    (29,'Condominium' , 'East Coast Condo' , 'Condo with unblocked view near East Coast',1880000 , 'Sold' , 'Freehold' , '469566' , '2003-03-22', '2003-01-05', 1313 , '45 Bedok Road S469566' , 4 , 3 , '2018-03-02',2), 
    (30,'Condominium' , 'High floor, North South facing house in Tampines' , '10 mins walk to Tampines Central, Bus Interchange, Tampines Hub, Tampines Mall, Century Square, Tampines One Mall',1850000 , 'Sold' , 'Freehold' , '528597' , '2012-10-15', '2012-09-08', 1496 , '51 Tampines Central 7 S528597' , 5 , 4 , '2019-09-05',3), 
    (31,'HDB' , '4 Room Flat in Aljunied' , 'Near to 3 MRT stations (Taiseng MRT, Woodleigh MRT, and Mattar MRT Stations) with 24-hour supermarket right downstairs',699000 , 'Available' , '99' , '360007' , '2015-11-07', '2015-07-06', 93 , 'District 13, Upper Aljunied Lane S360007' , 4 , 2 , '2020-01-07',4), 
    (32,'HDB' , '3 Bed House for Sale in Sengkang' , 'Walk-in wardrobe in the master bedroom with quality ceramic tiles in living/dining area and timber strip flooring in all 3 bedrooms',585000 , 'Available' , '99' , '544272' , '2008-05-20', '2008-01-29', 90 , '272D Sengkang Central S544272' , 4 , 2 , '2016-05-02',1), 
    (33,'HDB' , '2 Bed House for Sale in Punggol' , 'Walking distance to Punggol MRT, Waterway Point, bus interchange, Safra, future Punggol Town & Sports Hub', 402000 , 'Sold' , '99' , '821305' , '2010-04-24' , '2010-03-30', 68 , '305A Punggol Road S821305' , 3 , 2 , '2018-04-04',2), 
    (34,'HDB' , '2 Bed House for Sale in Strathmore with Garden View' , '8 Mins walking distance to Queenstown MRT & surrounded by plenty of amenities including schools, supermarkets, coffee shops', 560000 , 'Sold' , '99' , '143061' , '2010-07-06', '2010-04-22', 68 , '61B Strathmore Avenue S143061' , 3 , 2 , '2019-02-06',5) , 
    (35,'HDB' , '3 Bedroom flat with unblocked view in Bishan ' , 'Walking distance to Junction 8 and Bishan MRT & surrounded by Parks, Playground and PCN for cycling',900000, 'Sold' , '99' , '570166' , '2000-10-05', '1987-01-03', 122 , '166 Bishan Street 13 S570166' , 5 , 2 , '2018-01-05',6) , 
    (36,'HDB' , '3 Bedroom flat for Sale in Ang Mo Kio' , '6 Mins To Mayflower MRT, 1km From St Nicholas Girls',499000 , 'Available' , '99' , '560177' , '1981-03-09', '1980-09-11' , 91 , '177 Ang Mo Kio Avenue 4 S560177' , 4 , 2 , '2018-01-09',1) , 
    (37,'HDB' , '3 Bedroom flat with in Pasir Ris for Sale' , 'Less then 10 minutes to EATERIES/MARKET/SCHOOL with easy access to PIE/ TPE', 568000 , 'Sold' , '99' , '513526' , '2015-02-24', '2014-12-10', 93 , '526C Pasir Ris Street 51 S513526' , 4 , 2 , '2019-02-04',2) , 
    (38,'Condominium' , '4 Bed Condo for Sale in Lakepoint' , 'Minutes walk to Lakeside MRT, Amenities, Eateries and Schools', 2080000 , 'Sold' , '99' , '648923' , '1983-12-18', '1983-10-12', 3122 , '2 Lakepoint Drive S648923' , 5 , 4 , '2020-12-08',3) , 
    (39,'Condominium' , '2 Bed Freehold Condo for Sale in The Sound' , '5 minute walk to East Coast park & 2 min direct bus to Town', 1648888 , 'Available' , 'Freehold' , '429073' , '2014-07-25', '2014-04-04', 904 , '547 East Coast Road S429073' , 3 , 2 , '2019-07-02',4) ,
    (40,'Condominium' , '3 Bed Condo for Sale in SkyGreen Condo' , 'Minutes walk to Tai Seng, Macpherson and Bartley MRT & access to Full Condo Facilities',2280000 , 'Sold' , 'Freehold' , '368236' , '2016-09-22' , '2016-05-05', 1496 , '568 Macpherson Road S368236' , 4 , 3 , '2019-08-22',5);
"""
dummy_data["PropertyImage"] = """
    INSERT INTO PropertyImage(propertyId, path)
    VALUES 
    (1,'images/1/1.jpeg'),
    (1,'images/1/2.jpeg'),
    (1,'images/1/3.jpeg'),
    (2,'images/2/1.jpeg'),
    (2,'images/2/2.jpeg'),
    (2,'images/2/3.jpeg'),
    (2,'images/2/4.jpeg'),
    (3,'images/3/1.jpeg'),
    (3,'images/3/2.jpeg'),
    (3,'images/3/3.jpeg'),
    (3,'images/3/4.jpeg'),
    (4,'images/4/1.jpeg'),
    (4,'images/4/2.jpeg'),
    (4,'images/4/3.jpeg'),
    (4,'images/4/4.jpeg'),
    (5,'images/5/1.jpeg'),
    (5,'images/5/2.jpeg'),
    (5,'images/5/3.jpeg'),
    (5,'images/5/4.jpeg'),
    (6,'images/6/1.jpeg'),
    (6,'images/6/2.jpeg'),
    (6,'images/6/3.jpeg'),
    (6,'images/6/4.jpeg'),
    (7,'images/7/1.jpeg'),
    (7,'images/7/2.jpeg'),
    (7,'images/7/3.jpeg'),
    (7,'images/7/4.jpeg'),
    (8,'images/8/1.jpeg'),
    (8,'images/8/2.jpeg'),
    (8,'images/8/3.jpeg'),
    (8,'images/8/4.jpeg'),
    (9,'images/9/1.jpeg'),
    (9,'images/9/2.jpeg'),
    (9,'images/9/3.jpeg'),
    (9,'images/9/4.jpeg'),
    (10,'images/10/1.jpeg'),
    (10,'images/10/2.jpeg'),
    (10,'images/10/3.jpeg'),
    (10,'images/10/4.jpeg'),
    (11,'images/11/1.jpeg'),
    (11,'images/11/2.jpeg'),
    (11,'images/11/3.jpeg'),
    (11,'images/11/4.jpeg'),
    (12,'images/12/1.jpeg'),
    (12,'images/12/2.jpeg'),
    (12,'images/12/3.jpeg'),
    (12,'images/12/4.jpeg'),
    (13,'images/13/1.jpeg'),
    (13,'images/13/2.jpeg'),
    (13,'images/13/3.jpeg'),
    (13,'images/13/4.jpeg'),
    (14,'images/14/1.jpeg'),
    (14,'images/14/2.jpeg'),
    (14,'images/14/3.jpeg'),
    (14,'images/14/4.jpeg'),
    (15,'images/15/1.jpeg'),
    (15,'images/15/2.jpeg'),
    (15,'images/15/3.jpeg'),
    (15,'images/15/4.jpeg'),
    (16,'images/16/1.jpeg'),
    (16,'images/16/2.jpeg'),
    (16,'images/16/3.jpeg'),
    (16,'images/16/4.jpeg'),
    (17,'images/17/1.jpeg'),
    (17,'images/17/2.jpeg'),
    (17,'images/17/3.jpeg'),
    (17,'images/17/4.jpeg'),
    (18,'images/18/1.jpeg'),
    (18,'images/18/2.jpeg'),
    (18,'images/18/3.jpeg'),
    (18,'images/18/4.jpeg'),
    (19,'images/19/1.jpeg'),
    (19,'images/19/2.jpeg'),
    (19,'images/19/3.jpeg'),
    (19,'images/19/4.jpeg'),
    (20,'images/20/1.jpeg'),
    (20,'images/20/2.jpeg'),
    (20,'images/20/3.jpeg'),
    (20,'images/20/4.jpeg'),
    (21,'images/21/1.jpeg'),
    (21,'images/21/2.jpeg'),
    (21,'images/21/3.jpeg'),
    (21,'images/21/4.jpeg'),
    (22,'images/22/1.jpeg'),
    (22,'images/22/2.jpeg'),
    (22,'images/22/3.jpeg'),
    (22,'images/22/4.jpeg'),
    (23,'images/23/1.jpeg'),
    (23,'images/23/2.jpeg'),
    (23,'images/23/3.jpeg'),
    (23,'images/23/4.jpeg'),
    (24,'images/24/1.jpeg'),
    (24,'images/24/2.jpeg'),
    (24,'images/24/3.jpeg'),
    (24,'images/24/4.jpeg'),
    (25,'images/25/1.jpeg'),
    (25,'images/25/2.jpeg'),
    (25,'images/25/3.jpeg'),
    (25,'images/25/4.jpeg'),
    (26,'images/26/1.jpeg'),
    (26,'images/26/2.jpeg'),
    (26,'images/26/3.jpeg'),
    (26,'images/26/4.jpeg'),
    (27,'images/27/1.jpeg'),
    (27,'images/27/2.jpeg'),
    (27,'images/27/3.jpeg'),
    (27,'images/27/4.jpeg'),
    (28,'images/28/1.jpeg'),
    (28,'images/28/2.jpeg'),
    (28,'images/28/3.jpeg'),
    (28,'images/28/4.jpeg'),
    (29,'images/29/1.jpeg'),
    (29,'images/29/2.jpeg'),
    (29,'images/29/3.jpeg'),
    (29,'images/29/4.jpeg'),
    (30,'images/30/1.jpeg'),
    (30,'images/30/2.jpeg'),
    (30,'images/30/3.jpeg'),
    (31,'images/31/1.jpeg'),
    (31,'images/31/2.jpeg'),
    (31,'images/31/3.jpeg'),
    (31,'images/31/4.jpeg'),
    (32,'images/32/1.jpeg'),
    (32,'images/32/2.jpeg'),
    (32,'images/32/3.jpeg'),
    (32,'images/32/4.jpeg'),
    (33,'images/33/1.jpeg'),
    (33,'images/33/2.jpeg'),
    (33,'images/33/3.jpeg'),
    (33,'images/33/4.jpeg'),
    (34,'images/34/1.jpeg'),
    (34,'images/34/2.jpeg'),
    (34,'images/34/3.jpeg'),
    (34,'images/34/4.jpeg'),
    (35,'images/35/1.jpeg'),
    (35,'images/35/2.jpeg'),
    (35,'images/35/3.jpeg'),
    (35,'images/35/4.jpeg'),
    (36,'images/36/1.jpeg'),
    (36,'images/36/2.jpeg'),
    (36,'images/36/3.jpeg'),
    (37,'images/37/1.jpeg'),
    (37,'images/37/2.jpeg'),
    (37,'images/37/3.jpeg'),
    (37,'images/37/4.jpeg'),
    (38,'images/38/1.jpeg'),
    (38,'images/38/2.jpeg'),
    (38,'images/38/3.jpeg'),
    (38,'images/38/4.jpeg'),
    (39,'images/39/1.jpeg'),
    (39,'images/39/2.jpeg'),
    (39,'images/39/3.jpeg'),
    (39,'images/39/4.jpeg'),
    (40,'images/40/1.jpeg'),
    (40,'images/40/2.jpeg'),
    (40,'images/40/3.jpeg'),
    (40,'images/40/4.jpeg');

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

def update_parameters(query, params):
    try:
        conn = getDBConnection()
        if conn != None:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            # cursor.execute('SELECT last_insert_id()')
            result = cursor.fetchone()
            if result != None:
                return result[0]
    except Exception as e:
        print(f"DB Error occurred ({db_database}): {str(e)}")
        return None
    return None
