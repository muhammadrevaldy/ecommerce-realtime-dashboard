from pyathena import connect
import pandas as pd

conn = connect(
	s3_staging_dir = 's3://bucket-lks2026/transactions-athena/',
	region_name = 'ap-southeast-1',
	schema_name = 'ecommers'
)

query = "SELECT * FROM transaction LIMIT 5"

df = pd.read_sql(query, conn)
print (df)
