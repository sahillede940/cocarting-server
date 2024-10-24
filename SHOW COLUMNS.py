import mysql.connector

# Connect to the MySQL database and specify the database to use
mydb = mysql.connector.connect(
  host="cocarting-production-primary.cjwh4og1vbul.us-east-1.rds.amazonaws.com",
  user="root",
  password="adminadmin",
  database="cocarting"
)

# Get cursor
mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES")

# Display all rows
for row in mycursor:
    print(row)

# Close the cursor and connection
mycursor.close()
mydb.close()
