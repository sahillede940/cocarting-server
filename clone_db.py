import subprocess
import os
import mysql.connector
import shutil

# Database configurations for MySQL
STAGING_DB_CONFIG = {
    'host': 'localhost',        # Staging database host
    'user': 'root',        # Staging database username
    'password': 'postgres',  # Staging database password
    'database': 'cocarting_dummy'  # Staging database name
}


def create_staging_db():
    try:
        # Connect to MySQL server (without specifying a database)
        conn = mysql.connector.connect(
            host=STAGING_DB_CONFIG['host'],
            user=STAGING_DB_CONFIG['user'],
            password=STAGING_DB_CONFIG['password']
        )
        cursor = conn.cursor()

        # Create staging database if it does not exist
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {STAGING_DB_CONFIG['database']};")
        print("Staging database created or already exists")

    finally:
        cursor.close()
        conn.close()


def import_schema():
    print("Importing schema to staging database")
    # Adjust command with full path if mysql command is not in PATH
    command = [
        "mysql",
        "-h", STAGING_DB_CONFIG['host'],
        "-u", STAGING_DB_CONFIG['user'],
        f"--password={STAGING_DB_CONFIG['password']}",
        STAGING_DB_CONFIG['database']
    ]

    # Check if 'mysql' command exists in PATH, if not, set full path to `mysql.exe`
    # Change to actual path if needed
    mysql_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
    if not shutil.which("mysql"):
        command[0] = mysql_path

    try:
        with open("schema.sql", "rb") as file:
            result = subprocess.run(
                command, stdin=file, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print("Error importing schema:", result.stderr)
            else:
                print("Schema imported to staging database")
    except Exception as e:
        print("Failed to import schema:", e)


def main():
    # Step 1: Create staging database
    create_staging_db()

    # Step 2: Import schema into staging database
    import_schema()

    print("Schema replication to staging completed successfully")


if __name__ == "__main__":
    main()
