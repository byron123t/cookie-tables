import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow.parquet as pq
import pandas as pd


sizes = []
for region in ['eu', 'ca', 'us', 'can', 'za', 'sg', 'au', 'uk']:
    size = 0
    for mode in ['0k_20k']:
        df1 = pq.read_table('personal_info_data/{}/scan_{}_comply.parquet'.format(region, mode)).to_pandas()
        size += df1.shape[0]
    sizes.append(size)

df_data = {
 'Region': ['Ireland',
  'California',
  'Michigan',
  'Canada',
  'South Africa',
  'Singapore',
  'Australia',
  'United Kingdom'],
 'Inconsistent Cookies': [124,
  101,
  146,
  103,
  93,
  104,
  94,
  88,]}

df = pd.DataFrame(df_data)

sns.set(font_scale=1.05)
sns.set_style('whitegrid')
sns.catplot(data=df, y='Inconsistent Cookies', x='Region',            kind='bar', palette='colorblind')
sns.despine(left=True)
plt.xticks(rotation=90)
plt.subplots_adjust(top=0.85)
plt.suptitle('Cookie Consent Violations by Cookie Count', fontsize=16)
plt.savefig('plots/violations_ambiguous_cookies.pdf')



sizes = []
for region in ['eu', 'ca', 'us', 'can', 'za', 'sg', 'au', 'uk']:
    size = 0
    for mode in ['0k_20k']:
        df1 = pq.read_table('personal_info_data/{}/scan_{}_comply.parquet'.format(region, mode)).to_pandas()
        size += df1.shape[0]
    sizes.append(size)

df_data = {
 'Region': [
  'Ireland',
  'California',
  'Michigan',
  'Canada',
  'South Africa',
  'Singapore',
  'Australia',
  'United Kingdom'],
 'Websites with Consent Violations (%)': [
  4.53,
  4.81,
  5.58,
  4.89,
  5.05,
  4.93,
  5.00,
  4.20]}

df = pd.DataFrame(df_data)

sns.set(font_scale=1.05)
sns.set_style('whitegrid')
sns.catplot(data=df, y='Websites with Consent Violations (%)', x='Region',
            kind='bar', palette='colorblind')
sns.despine(left=True)
plt.subplots_adjust(top=0.85)
plt.xticks(rotation=90)
plt.suptitle('Cookie Consent Violations by Cookie Count', fontsize=16)
plt.savefig('plots/violations_ambiguous_website.pdf')