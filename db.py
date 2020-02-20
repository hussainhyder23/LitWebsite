#!/usr/bin/python3
import pymysql as psq

# Open database connection
db = psq.connect("localhost","ccdAdmin","hello123","ccd" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method

# Create table as per requirement
sql = """CREATE TABLE registrations(
   register_id INT AUTO_INCREMENT PRIMARY KEY,
   firstname VARCHAR(40),
   lastname VARCHAR(40),
   email VARCHAR(200),
   phone_no VARCHAR(15),
   college VARCHAR(100),
   year INT,
   branch VARCHAR(10),
   events VARCHAR(200)
);
"""

cursor.execute(sql)

sql = """CREATE TABLE messages(
   message_id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(100),
   email VARCHAR(200),
   message VARCHAR(2000)
);
"""

cursor.execute(sql)

# disconnect from server
db.close()
