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

# Define the email to search
email_to_search = "sahillede940@gmail.com"  # Replace with the actual email you want to search for

# Search by email
try:
    # Execute query to search by email
    mycursor.execute(f"SELECT * FROM users WHERE email = {email_to_search}")
    result = mycursor.fetchall()
    
    # Check if any results were found
    if result:
        for row in result:
            print(row)
    else:
        print("No records found with the specified email.")

except mysql.connector.Error as err:
    print("Error:", err)

# Close the cursor and connection
mycursor.close()
mydb.close()
