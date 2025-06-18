import os
import re
import duckdb
from datetime import datetime
from pathlib import Path

# Configuration
INPUT_FOLDER = '../data/in'  # Folder to store csv files to ingest
ARCHIVE_FOLDER = '../data/arc'  # Folder to store processed csv files
DB_FILE = 'citibike.duckdb'  # DuckDB database file
TABLE_NAME = 'raw_citibike_trip_data'  # Table name in DuckDB

# Create folders if they don't exist
Path(INPUT_FOLDER).mkdir(exist_ok=True)
Path(ARCHIVE_FOLDER).mkdir(exist_ok=True)

# return sorted list of valid filenames
def get_citibike_files():
    """Return a sorted list of CitiBike CSV files with dates in YYYYMM format"""
    pattern = re.compile(r'.*?(\d{6})-citibike-tripdata.*?\.csv$')
    files = []
    for filename in os.listdir(INPUT_FOLDER):
        match = pattern.search(filename)
        if match:
            print(f"Match found: {filename}")  # Extracts the 8 digits (e.g., "20230115")
            date_str = match.group(1)
            try:
                date = datetime.strptime(date_str, '%Y%m').date()
                files.append((date, filename))
            except ValueError:
                continue
        else:
            print(f"No match: {filename}")
    files.sort()
    return [filename for date, filename in files]

# Load CSV data to duckdb
def load_to_duckdb(filename):
    """Load CSV file to DuckDB with upsert functionality"""
    filepath = os.path.join(INPUT_FOLDER, filename)
    current_datetime = datetime.now()
    before_count = 0

    # Define the schema for CSV import
    csv_schema = {
        'ride_id': 'VARCHAR',
        'rideable_type': 'VARCHAR',
        'started_at': 'TIMESTAMP',
        'ended_at': 'TIMESTAMP',
        'start_station_name': 'VARCHAR',
        'start_station_id': 'VARCHAR',
        'end_station_name': 'VARCHAR',
        'end_station_id': 'VARCHAR',
        'start_lat': 'VARCHAR',
        'start_lng': 'VARCHAR',
        'end_lat': 'VARCHAR',
        'end_lng': 'VARCHAR',
        'member_casual': 'VARCHAR'
    }
    
    with duckdb.connect(DB_FILE) as conn:
        # First check if table exists
        table_exists = conn.execute(
            f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{TABLE_NAME}'"
        ).fetchone()[0] > 0
        
        if not table_exists:
            # Create table with proper schema if it doesn't exist
            conn.execute(f"""
            CREATE TABLE {TABLE_NAME} AS
            SELECT *, 
                   CURRENT_TIMESTAMP AS insert_datetime,
                   '{filename}' AS source_file
            FROM read_csv('{filepath}', header=true, auto_detect=true, types={csv_schema})
            """)
            
            # Add primary key constraint
            conn.execute(f"ALTER TABLE {TABLE_NAME} ADD PRIMARY KEY (ride_id)")
        else:
            # Table exists - perform upsert operation
            conn.execute(f"""
            CREATE TEMPORARY TABLE temp_data AS
            SELECT *, 
                   CURRENT_TIMESTAMP AS insert_datetime,
                   '{filename}' AS source_file
            FROM read_csv('{filepath}', header=true, auto_detect=true, types={csv_schema})
            """)

            # Get counts before operation
            before_count = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
            
            # Perform upsert (insert or replace) based on ride_id
            conn.execute(f"""
            INSERT OR REPLACE INTO {TABLE_NAME}
            SELECT * FROM temp_data
            """)
            
            # Clean up temporary table
            conn.execute("DROP TABLE temp_data")
        
        # Archive file
        archive_path = os.path.join(ARCHIVE_FOLDER, filename)
        os.rename(filepath, archive_path)

        final_count = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]

        print(f">>> Processing file: {filename}\n")
        print(f"Processing time: {current_datetime}\n")
        print(f"Total rows in database before operation: {before_count}\n")
        print(f"Total rows in database after operation: {final_count}\n")

def main():
    print("Starting CitiBike data import process...\n")
    files = get_citibike_files()
    if not files:
        print("No CitiBike files found to process.\n")
        return
    
    print(f"Found {len(files)} files to process.\n")
    
    for filename in files:
        load_to_duckdb(filename)

    print("\nProcessing complete.")

if __name__ == '__main__':
    main()