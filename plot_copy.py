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

df_data = {'Consent Violation Type': ['Rejected Cookie Usage',
  'Rejected Cookie Usage',
  'Rejected Cookie Usage',
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
  'Consent Choice Omission',
  'Consent Choice Omission'],
 'Region': ['Ireland',
  'California',
  'Michigan',
  'Canada',
  'South Africa',
  'Singapore',
  'Australia',
  'United Kingdom',
  'Ireland',
  'California',
  'Michigan',
  'Canada',
  'South Africa',
  'Singapore',
  'Australia',
  'United Kingdom'],
 'Inconsistent Cookies': [11034,
  16417,
  15052,
  14163,
  12998,
  12660,
  12993,
  10662,
  14568,
  29725,
  36677,
  29309,
  26637,
  23981,
  24963,
  14920]}

df = pd.DataFrame(df_data)

sns.set(font_scale=1.05)
sns.set_style('whitegrid')
sns.catplot(data=df, y='Inconsistent Cookies', hue='Region', x='Consent Violation Type',
            kind='bar', palette='colorblind')
sns.despine(left=True)
plt.subplots_adjust(top=0.85)
plt.suptitle('Cookie Consent Violations by Cookie Count', fontsize=16)
plt.savefig('plots/violations.pdf')






# import matplotlib.pyplot as plt
# import seaborn as sns
# import pyarrow.parquet as pq
# import pandas as pd


# sizes = []
# for region in ['eu', 'ca', 'us', 'can', 'za', 'sg', 'au', 'uk']:
#     size = 0
#     for mode in ['0k_20k']:
#         df1 = pq.read_table('personal_info_data/{}/scan_{}_comply.parquet'.format(region, mode)).to_pandas()
#         size += df1.shape[0]
#     sizes.append(size)

# df_data = {'Consent Violation Type': ['Rejected Cookie Usage',
#   'Rejected Cookie Usage',
#   'Rejected Cookie Usage',
#   'Rejected Cookie Usage',
#   'Rejected Cookie Usage',
#   'Rejected Cookie Usage',
#   'Rejected Cookie Usage',
#   'Rejected Cookie Usage',
#   'Consent Choice Omission',
#   'Consent Choice Omission',
#   'Consent Choice Omission',
#   'Consent Choice Omission',
#   'Consent Choice Omission',
#   'Consent Choice Omission',
#   'Consent Choice Omission',
#   'Consent Choice Omission'],
#  'Region': ['Ireland',
#   'California',
#   'Michigan',
#   'Canada',
#   'South Africa',
#   'Singapore',
#   'Australia',
#   'United Kingdom',
#   'Ireland',
#   'California',
#   'Michigan',
#   'Canada',
#   'South Africa',
#   'Singapore',
#   'Australia',
#   'United Kingdom'],
#  'Websites with Consent Violations (%)': [82.58,
#   86.22,
#   80.76,
#   80.07,
#   79.32,
#   77.52,
#   77.33,
#   81.57,
#   88.55,
#   93.47,
#   93.13,
#   92.44,
#   91.14,
#   92.07,
#   92.10,
#   89.56]}

# df = pd.DataFrame(df_data)

# sns.set(font_scale=1.1)
# sns.set_style('whitegrid')
# sns.catplot(data=df, y='Websites with Consent Violations (%)', hue='Region', x='Consent Violation Type',
#             kind='bar', palette='colorblind')
# sns.despine(left=True)
# plt.subplots_adjust(top=0.85)
# plt.ylim(50, 100)
# plt.suptitle('Websites with Consent Violations', fontsize=16)
# plt.savefig('plots/websiteviolations.pdf')
