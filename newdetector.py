import re, os, base64
import pandas as pd
import pyarrow.parquet as pq
from tqdm import tqdm
import numpy as np
from matplotlib import pyplot as plt


regions = ['ca', 'eu', 'uk', 'au', 'us', 'sg', 'can', 'za']
mode = '0k_20k'

def calculate_metrics(df):
    total_cookies = len(df)
    
    third_party_cookies = df[~df.apply(lambda x: x['site'] in x['domain'], axis=1)]
    
    omit_errors = df[df['comply'] == 'omit']
    comply_errors = df[df['comply'] == 'comply']
    incorrect_errors = df[df['comply'] == 'incorrect']
    ambiguous_errors = df[df['comply'] == 'ambiguous']
    third_party_omit_errors = third_party_cookies[third_party_cookies['comply'] == 'omit']
    third_party_comply_errors = third_party_cookies[third_party_cookies['comply'] == 'comply']
    third_party_incorrect_errors = third_party_cookies[third_party_cookies['comply'] == 'incorrect']
    third_party_ambiguous_errors = third_party_cookies[third_party_cookies['comply'] == 'ambiguous']

    metrics = {
        'total_cookies': total_cookies,
        'total_incorrect_errors': len(incorrect_errors),
        'total_ambiguous_errors': len(ambiguous_errors),
        'total_omit_errors': len(omit_errors),
        'total_comply': len(comply_errors),
        'total_comply_percentage': len(comply_errors) / total_cookies * 100 if total_cookies > 0 else 0,
        'total_incorrect_percentage': len(incorrect_errors) / total_cookies * 100 if total_cookies > 0 else 0,
        'total_ambiguous_percentage': len(ambiguous_errors) / total_cookies * 100 if total_cookies > 0 else 0,
        'total_omit_percentage': len(omit_errors) / total_cookies * 100 if total_cookies > 0 else 0,
        'third_party_cookies': len(third_party_cookies),
        'third_party_comply_errors': len(third_party_comply_errors),
        'third_party_comply': len(third_party_comply_errors),
        'third_party_incorrect_errors': len(third_party_incorrect_errors),
        'third_party_ambiguous_errors': len(third_party_ambiguous_errors),
        'third_party_omit_errors': len(third_party_omit_errors),
        'third_party_comply_percentage': len(third_party_comply_errors) / len(third_party_cookies) * 100 if len(third_party_cookies) > 0 else 0,
        'third_party_incorrect_errors_percentage': len(third_party_incorrect_errors) / len(third_party_cookies) * 100 if len(third_party_cookies) > 0 else 0,
        'third_party_ambiguous_errors_percentage': len(third_party_ambiguous_errors) / len(third_party_cookies) * 100 if len(third_party_cookies) > 0 else 0,
        'third_party_omit_errors_percentage': len(third_party_omit_errors) / len(third_party_cookies) * 100 if len(third_party_cookies) > 0 else 0,
    }

    return metrics

# Dataframe to hold metrics for all regions
metrics_df = pd.DataFrame()

# Process each region
for region in regions:
    try:
        df = pq.read_table(f'personal_info_data/{region}/scan_{mode}_comply.parquet').to_pandas()
        region_metrics = calculate_metrics(df)
        region_metrics['region'] = region
        metrics_df = metrics_df.append(region_metrics, ignore_index=True)
    except Exception as e:
        print(f"Failed to process region {region}: {e}")

# Ensure that the metrics DataFrame has the required columns before converting to numeric
expected_columns = ['total_cookies', 'total_incorrect_errors', 'total_ambiguous_errors', 'total_omit_errors', 'total_comply', 'total_comply_percentage', 'total_incorrect_percentage', 'total_ambiguous_percentage', 'total_omit_percentage', 'third_party_cookies', 'third_party_comply_errors', 'third_party_comply', 'third_party_incorrect_errors', 'third_party_ambiguous_errors', 'third_party_omit_errors', 'third_party_comply_percentage', 'third_party_incorrect_errors_percentage', 'third_party_ambiguous_errors_percentage', 'third_party_omit_errors_percentage']
for col in expected_columns:
    if col not in metrics_df.columns:
        metrics_df[col] = 0

metrics_df[['total_cookies', 'total_incorrect_errors', 'total_ambiguous_errors', 'total_omit_errors', 'total_comply', 'total_comply_percentage', 'total_incorrect_percentage', 'total_ambiguous_percentage', 'total_omit_percentage', 'third_party_cookies', 'third_party_comply_errors', 'third_party_comply', 'third_party_incorrect_errors', 'third_party_ambiguous_errors', 'third_party_omit_errors', 'third_party_comply_percentage', 'third_party_incorrect_errors_percentage', 'third_party_ambiguous_errors_percentage', 'third_party_omit_errors_percentage']] = metrics_df[['total_cookies', 'total_incorrect_errors', 'total_ambiguous_errors', 'total_omit_errors', 'total_comply', 'total_comply_percentage', 'total_incorrect_percentage', 'total_ambiguous_percentage', 'total_omit_percentage', 'third_party_cookies', 'third_party_comply_errors', 'third_party_comply', 'third_party_incorrect_errors', 'third_party_ambiguous_errors', 'third_party_omit_errors', 'third_party_comply_percentage', 'third_party_incorrect_errors_percentage', 'third_party_ambiguous_errors_percentage', 'third_party_omit_errors_percentage']].apply(pd.to_numeric)

print(metrics_df)

for col in expected_columns:
    print(col)
    print(metrics_df[col])

fig, axes = plt.subplots(5, 2, figsize=(14, 10))

axes[0, 0].bar(metrics_df['region'], metrics_df['total_cookies'])
axes[0, 0].set_title('Total Cookies per Region')
axes[0, 0].set_ylabel('Total Cookies')

# Total Comply
axes[0, 1].bar(metrics_df['region'], metrics_df['total_comply_percentage'])
axes[0, 1].set_title('Total Comply per Region')
axes[0, 1].set_ylabel('Total Comply')

# Total Comply Errors Percentage
axes[1, 0].bar(metrics_df['region'], metrics_df['total_omit_percentage'])
axes[1, 0].set_title('Total Omit Errors Percentage per Region')
axes[1, 0].set_ylabel('Omit Errors Percentage')

# Total Incorrect Errors Percentage
axes[1, 1].bar(metrics_df['region'], metrics_df['total_incorrect_percentage'])
axes[1, 1].set_title('Total Incorrect Errors Percentage per Region')
axes[1, 1].set_ylabel('Incorrect Errors Percentage')

# Total Ambiguous Errors Percentage
axes[2, 0].bar(metrics_df['region'], metrics_df['total_ambiguous_percentage'])
axes[2, 0].set_title('Total Ambiguous Errors Percentage per Region')
axes[2, 0].set_ylabel('Ambiguous Errors Percentage')

# Third Party Cookies
axes[2, 1].bar(metrics_df['region'], metrics_df['third_party_cookies'])
axes[2, 1].set_title('Third Party Cookies per Region')
axes[2, 1].set_ylabel('Third Party Cookies')

# Third Party Comply
axes[3, 0].bar(metrics_df['region'], metrics_df['third_party_comply_percentage'])
axes[3, 0].set_title('Third Party Comply per Region')
axes[3, 0].set_ylabel('Third Party Comply')

# Third Party Comply Errors Percentage
axes[3, 1].bar(metrics_df['region'], metrics_df['third_party_omit_errors_percentage'])
axes[3, 1].set_title('Third Party Omit Errors Percentage per Region')
axes[3, 1].set_ylabel('Omit Errors Percentage')

# Third Party Incorrect Errors Percentage
axes[4, 0].bar(metrics_df['region'], metrics_df['third_party_incorrect_errors_percentage'])
axes[4, 0].set_title('Third Party Incorrect Errors Percentage per Region')
axes[4, 0].set_ylabel('Incorrect Errors Percentage')

# Third Party Ambiguous Errors Percentage
axes[4, 1].bar(metrics_df['region'], metrics_df['third_party_ambiguous_errors_percentage'])
axes[4, 1].set_title('Third Party Ambiguous Errors Percentage per Region')
axes[4, 1].set_ylabel('Ambiguous Errors Percentage')

plt.tight_layout()
plt.savefig('plots/cookies_metrics.pdf')