import re, os, base64
import pandas as pd
import pyarrow.parquet as pq
from tqdm import tqdm
import numpy as np


def contains_personal_information(cookie):
    tracker_keywords = ['tracker', 'track', 'trck', 'advertising', 'identifier', 'id', '_gid,', '_uuid' 'user_id', 'session']
    location_keywords = ['location', 'latitude', 'longitude', 'city', 'country', 'postal', 'address', 'geo', 'united-kingdom', 'united kingdom', 'united_kingdom', 'california', 'united states', 'united-states', 'united_states', 'germany', 'great-britain', 'great_britain', 'great britain', 'ec2n 3ar', '60323', '95051', 'santa clara', 'santa-clara', 'santa_clara', 'london', 'frankfurt']
    ip_address_keywords = ['ip_address', 'ip-address', 'ip']
    demographic_keywords = ['gender', 'income', 'demographic', 'race', 'ethnicity']

    tracker_patterns = [
        r'(?i)utm_[a-z]+',  # UTM parameters
        r'[a-fA-F0-9]{8}(-|\.)([a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}', # UUID
        r'^GA\d\.\d\.\d+\.\d+$', # Google Analytics ID
        r'^fb\d\.\d\.\d+\.\d+$', # Facebook Pixel ID
    ]

    location_patterns = r'-?(\d+\.\d+),\s*-?(\d+\.\d+)'

    ip_address_patterns = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    for column in cookie:
        if any(keyword in str(column).lower() for keyword in demographic_keywords):
            return 'demographic'
        if any(keyword in str(column).lower() for keyword in ip_address_keywords):
            return 'ip_address'
        if any(keyword in str(column).lower() for keyword in location_keywords):
            return 'location'
        if any(keyword in str(column).lower() for keyword in tracker_keywords):
            return 'tracker'

        if re.search(ip_address_patterns, str(column)):
            return 'ip_address'
        if re.search(location_patterns, str(column)):
            return 'location'
        if any(re.search(pattern, str(column)) for pattern in tracker_patterns):
            return 'tracker'
        if len(str(column)) > 50:
            return 'likely_tracker'
        
        try:
            decoded_string = base64.b64decode(str(column)).decode('utf-8')
            if any(keyword in decoded_string.lower() for keyword in demographic_keywords):
                return 'demographic'
            if any(keyword in decoded_string.lower() for keyword in ip_address_keywords):
                return 'ip_address'
            if any(keyword in decoded_string.lower() for keyword in location_keywords):
                return 'location'
            if any(keyword in decoded_string.lower() for keyword in tracker_keywords):
                return 'tracker'

            if re.search(ip_address_patterns, decoded_string):
                return 'ip_address'
            if re.search(location_patterns, decoded_string):
                return 'location'
            if any(re.search(pattern, decoded_string) for pattern in tracker_patterns):
                return 'tracker'
        except Exception:
            pass

    return 'False'


# parquet_file = 'sample.parquet'
# df = pq.read_table(parquet_file).to_pandas()
# df['contains_personal_info'] = df.apply(contains_personal_information, axis=1)
# df.to_parquet('sample_detected1.parquet')

for region in ['eu', 'ca', 'us', 'can', 'za', 'sg', 'au', 'uk']:
    size_comply = 0
    size_omit = 0
    size_incorrect = 0
    size_ambiguous = 0
    size_total = 0
    size_omit1 = 0
    size_omit2 = 0
    size_incorrect1 = 0
    size_incorrect2 = 0
    size_ambiguous1 = 0
    size_ambiguous2 = 0
    size_comply1 = 0
    size_comply2 = 0
    size_total_personal = 0
    size_ip = 0
    size_location = 0
    size_tracker = 0
    size_demographic = 0
    sites_noncompliant = 0
    sites_total = 0
    for mode in ['0k_20k']:
        df1 = pq.read_table('personal_info_data/{}/scan_{}_comply.parquet'.format(region, mode)).to_pandas()
        df1 = df1.dropna()
        size_total += df1.shape[0]
        df2 = df1.where(((df1['comply'] == 'comply'))).dropna()
        size_comply += df2.shape[0]
        size_comply1 += df2.shape[0]
        df2 = df2.where(((df2['contains_personal_info'] != 'False'))).dropna()
        size_comply2 += df2.shape[0]
        df2 = df1.where(((df1['comply'] == 'omit'))).dropna()
        size_omit += df2.shape[0]
        size_omit1 += df2.shape[0]
        df2 = df2.where(((df2['contains_personal_info'] != 'False'))).dropna()
        size_omit2 += df2.shape[0]
        df2 = df1.where(((df1['comply'] == 'incorrect'))).dropna()
        size_incorrect += df2.shape[0]
        size_incorrect1 += df2.shape[0]
        df2 = df2.where(((df2['contains_personal_info'] != 'False'))).dropna()
        size_incorrect2 += df2.shape[0]
        df2 = df1.where(((df1['comply'] == 'ambiguous'))).dropna()
        size_ambiguous += df2.shape[0]
        size_ambiguous1 += df2.shape[0]
        df2 = df2.where(((df2['contains_personal_info'] != 'False'))).dropna()
        size_ambiguous2 += df2.shape[0]

        df2 = df1['site'].drop_duplicates().dropna()
        sites_total += df2.shape[0]
    # for mode in ['0k_20k']:
    #     df1 = pq.read_table('personal_info_data/{}/scan_{}_comply.parquet'.format(region, mode)).to_pandas()
    #     df1 = df1.dropna()
    df2 = df1.where(((df1['comply'] != 'comply'))).dropna()
    df2 = df2.drop_duplicates(['site']).dropna()
    df3 = df2.where(((df2['contains_personal_info'] == 'ip_address'))).dropna()
    size_ip = df3.shape[0]
    df3 = df2.where(((df2['contains_personal_info'] == 'location'))).dropna()
    size_location = df3.shape[0]
    df3 = df2.where(((df2['contains_personal_info'] == 'tracker'))).dropna()
    size_tracker = df3.shape[0]
    df3 = df2.where(((df2['contains_personal_info'] == 'demographic'))).dropna()
    size_demographic = df3.shape[0]
    df3 = df2.where(((df2['contains_personal_info'] == 'likely_tracker'))).dropna()
    size_tracker += df3.shape[0]
    df3 = df2.where(((df2['contains_personal_info'] == 'False'))).dropna()
    size_none = df3.shape[0]
    
    # print('{}, comply: {}'.format(region, size_comply / size_total))
    # print('{}, omit: {}'.format(region, size_omit / size_total))
    # print('{}, incorrect: {}'.format(region, size_incorrect / size_total))
    # print('{}, ambiguous: {}'.format(region, size_ambiguous / size_total))
    size_total_personal = size_none + size_ip + size_location + size_tracker
    # print('{}, omit: {}'.format(region, (size_omit2 / size_omit1) * 100))
    # print('{}, incorrect: {}'.format(region, (size_incorrect2 / size_incorrect1) * 100))
    # print('{}, ambiguous: {}'.format(region, (size_ambiguous2 / size_ambiguous1) * 100))
    # print('{}, comply: {}'.format(region, (size_comply2 / size_comply1) * 100))
    print('{}, ip_address: {}'.format(region, (size_ip / size_total_personal) * 100))
    print('{}, location: {}'.format(region, (size_location / size_total_personal) * 100))
    print('{}, tracker: {}'.format(region, (size_tracker / size_total_personal) * 100))
    print('{}, none: {}'.format(region, (size_none / size_total_personal) * 100))
    # print('{}, demographic: {}'.format(region, (size_demographic / size_total_personal) * 100))

        # # df1['contains_personal_info'] = df1.apply(contains_personal_information, axis=1)
        # # df1.to_parquet('personal_info_data/{}/scan_{}_comply.parquet'.format(region, mode))
        

        # df1 = pq.read_table('personal_info_data/{}/all_complies_{}.parquet'.format(region, mode)).to_pandas()
        # df2 = pq.read_table('personal_info_data/{}/scan_{}.parquet'.format(region, mode)).to_pandas()
        # df2 = df2.reset_index(drop=True)
        # df2 = df2.drop_duplicates(subset=['name', 'domain', 'site'])
        # df2 = df2.drop(['path', 'expires', 'size', 'httpOnly', 'secure', 'session', 'sameSite', 'priority', 'sameParty', 'sourceScheme', 'sourcePort', 'request_url', 'page_url'], axis=1)
        # print(df2)
        # for index, row in tqdm(df1.iterrows(), total=df1.shape[0]):
        #     criteria = (row['name'] == df2['name']) & (row['domain'] == df2['domain']) & (row['site'] == df2['site'])
        #     df2.loc[criteria, 'comply'] = row['comply']
        # df2['contains_personal_info'] = df2.apply(contains_personal_information, axis=1)
        # df2.to_parquet('personal_info_data/{}/scan_{}_comply.parquet'.format(region, mode))
