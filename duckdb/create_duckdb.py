import duckdb

# Connect to or create a DuckDB file
conn = duckdb.connect('raw_citibike_trip.duckdb')

# Load CSV directly into a table
conn.execute("""
    CREATE TABLE raw_citibike_trip AS 
    SELECT * FROM read_csv('../data/JC-202505-citibike-tripdata-testdata.csv', 
                          header=true, 
                          auto_detect=true)
""")


# Verify
print(conn.execute("SELECT COUNT(*) FROM raw_citibike_trip").fetchall())

# print(conn.execute("DESCRIBE raw_citibike_trip").fetchall())

# Close connection (saves the database)
conn.close()