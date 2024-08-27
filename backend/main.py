import duckdb
import pandas as pd

# Connect to DuckDB
con = duckdb.connect()

# Query Parquet file and convert result to DataFrame
df = con.execute("SELECT * FROM read_parquet('./test-data/sample1.parquet')").df()

# Convert DataFrame to JSON-compatible format (dictionary)
json_data = df.to_dict(orient='records')

# Test with print
print(df)
print(json_data)
