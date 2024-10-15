import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow.parquet as pq
import pandas as pd


sizes = []
for region in ['ca', 'eu', 'uk', 'au', 'us', 'sg', 'can', 'za']:
    size = 0
    for mode in ['0k_20k']:
        df1 = pq.read_table('personal_info_data/{}/scan_{}_comply.parquet'.format(region, mode)).to_pandas()
        size += df1.shape[0]
    sizes.append(size)

df_data = {'Consent Violation Type': ['Rejected Cookie Usage',
  'Rejected Cookie Usage',
  'Rejected Cookie Usage',
  'Rejected Cookie Usage',
  'Rejected Cookie Usage',
  'Rejected Cookie Usage',
  'Consent Choice Omission',
  'Consent Choice Omission',
  'Consent Choice Omission',
  'Consent Choice Omission',
  'Consent Choice Omission',
  'Consent Choice Omission',
  'Ambiguous Consent',
  'Ambiguous Consent',
  'Ambiguous Consent',
  'Ambiguous Consent',
  'Ambiguous Consent',
  'Ambiguous Consent'],
 'Region': ['Germany',
  'Germany',
  'California',
  'California',
  'United Kingdom',
  'United Kingdom',
  'Germany',
  'Germany',
  'California',
  'California',
  'United Kingdom',
  'United Kingdom',
  'Germany',
  'Germany',
  'California',
  'California',
  'United Kingdom',
  'United Kingdom'],
 'Measurement': ['Cookies',
  'Websites',
  'Cookies',
  'Websites',
  'Cookies',
  'Websites',
  'Cookies',
  'Websites',
  'Cookies',
  'Websites',
  'Cookies',
  'Websites',
  'Cookies',
  'Websites',
  'Cookies',
  'Websites',
  'Cookies',
  'Websites'],
 'Quantity': [(34604 / sizes[0]) * 100,
  82.78,
  (53739 / sizes[1]) * 100,
  86.6,
  (34981 / sizes[2]) * 100,
  82.82,
  (42917 / sizes[0]) * 100,
  84.46,
  (93249 / sizes[1]) * 100,
  90.57,
  (43878 / sizes[2]) * 100,
  85.44,
  (350 / sizes[0]) * 100,
  4.1,
  (387 / sizes[1]) * 100,
  4.38,
  (373 / sizes[2]) * 100,
  4.05]}

df = pd.DataFrame(df_data)

sns.set_style('whitegrid')
sns.catplot(data=df, x='Region', y='Quantity', hue='Measurement', col='Consent Violation Type',
            kind='bar', palette='colorblind', height=4, aspect=1)
sns.despine(left=True)
plt.subplots_adjust(top=0.85)
plt.suptitle('Detected consent violations of cookie usage', fontsize=16)
plt.savefig('plots/violations.pdf')
