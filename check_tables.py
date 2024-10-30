from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables
load_dotenv()

# Retrieve database connection details from environment variables
DB_CONNECTION = os.getenv("DB_CONNECTION")  # Should be 'mariadb'
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# URL encode the password
encoded_password = urllib.parse.quote(DB_PASSWORD)

# Construct the database URL using the correct dialect for MariaDB
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# Create the engine with the server version specified (replace with your actual version)
engine = create_engine(
    DATABASE_URL,
    connect_args={"server_version": "10.5"},  # Update to your MariaDB version
    echo=True  # Enable logging for debugging purposes
)

# Create MetaData instance
metadata = MetaData()

# Reflect the tables, disabling foreign key reflection
metadata.reflect(bind=engine, resolve_fks=False)

# Use automap_base with the existing metadata
Base = automap_base(metadata=metadata)

# Prepare the classes
Base.prepare()

# Print reflected table names to verify
print("Reflected tables:", Base.classes.keys())

# Check if specific tables are present
expected_tables = ["users", "products", "product_images", "cocarts", "cocart_products"]
for table in expected_tables:
    if table in Base.classes:
        print(f"Table '{table}' found!")
    else:
        print(f"Table '{table}' NOT found.")
