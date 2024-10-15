import re, os
import pandas as pd
import pyarrow.parquet as pq
from tqdm import tqdm
from api import OpenAIChatSession


oai = OpenAIChatSession()
parquet_file = 'sample.parquet'
df = pq.read_table(parquet_file).to_pandas()
existing_parquet = 'cookies.parquet'
if os.path.exists(existing_parquet):
    existing_df = pq.read_table(existing_parquet).to_pandas()
    existing = True
else:
    existing = False
new_data = []

pbar = tqdm(df.iterrows(), total=df.shape[0])
tracking_value = 0.0
total_count = 0
for index, row in pbar:
    total_count += 1
    if existing and total_count <= existing_df.shape[0]:
        if existing_df.iloc[total_count - 1]['contains_personal_info']:
            tracking_value += 1
        pbar.set_description(f"Tracking value: {tracking_value / total_count}")
        new_data.append(existing_df.iloc[total_count - 1])
        new_df = pd.DataFrame(new_data)
        new_df.to_parquet('cookies.parquet')
    else:
        response = oai.handle_response(str((row['name'], row['value'])))
        if 'YES' in response:
            row['contains_personal_info'] = True
        else:
            row['contains_personal_info'] = False
        if row['contains_personal_info']:
            tracking_value += 1
        pbar.set_description(f"Tracking value: {tracking_value / total_count}")
        new_data.append(row)
        new_df = pd.DataFrame(new_data)
        new_df.to_parquet('cookies.parquet')
