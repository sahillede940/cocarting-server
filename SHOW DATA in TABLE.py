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
mycursor.execute("SELECT * FROM cocarts")

# Fetch column names from the description attribute
column_names = [i[0] for i in mycursor.description]
print("Column names:", column_names)

# Display all rows
for row in mycursor:
    print(row)
    break

# Close the cursor and connection
mycursor.close()
mydb.close()
