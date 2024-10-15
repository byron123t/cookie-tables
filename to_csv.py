import pyarrow.parquet as pq
import pandas as pd


existing_parquet = 'cookies.parquet'
existing_df = pq.read_table(existing_parquet).to_pandas()
existing_df.to_csv('cookies.csv')

# existing_parquet = 'ca_scan_0k_20k.parquet'
# existing_df = pq.read_table(existing_parquet).to_pandas()
# existing_df.sample(frac=0.01).to_parquet('sample.parquet')