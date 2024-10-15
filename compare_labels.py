import pyarrow.parquet as pq
import pandas as pd


ground_truth = []

with open('ground_truth.txt', 'r') as infile:
    for line in infile:
        if line.strip().lower() == 'true':
            ground_truth.append(True)
        else:
            ground_truth.append(False)

parquet_file = 'sample_detected1.parquet'
df1 = pq.read_table(parquet_file).to_pandas()
# existing_parquet = 'cookies.parquet'
existing_parquet = 'backup_cookies.parquet'
df2 = pq.read_table(existing_parquet).to_pandas()
data = []
bools = []
bool2 = []
df3 = pd.DataFrame()

for val1, val2, val3 in zip(df2.iterrows(), df1.iterrows(), ground_truth):
    val1[1]['contains_personal_info_detector'] = val2[1]['contains_personal_info']
    val1[1]['contains_personal_info_gt'] = val3
    data.append(val1[1])
    bools.append(val1[1]['contains_personal_info'])
    if val1[1]['contains_personal_info_detector'] != 'False':
        bool2.append(True)
    else:
        bool2.append(False)
    # bool2.append(val1[1]['contains_personal_info_detector'])
    # bools.append(val2[1]['contains_personal_info'])

# for val1, val2 in zip(df2.iterrows(), df1.iterrows()):
#     val1[1]['contains_personal_info_detector'] = val2[1]['contains_personal_info']
#     data.append(val1[1])
#     bools.append(val1[1]['contains_personal_info'])
#     bool2.append(val1[1]['contains_personal_info_detector'])
#     # bools.append(val2[1]['contains_personal_info'])

print(df2.shape[0])
print(len(ground_truth))
df3 = pd.DataFrame(data)
df3.to_csv('new_annotate_cookies.csv')

tp = 0
fp = 0
tn = 0
fn = 0
total = 0
for val1, val2 in zip(ground_truth, bool2):
    if val2 and val1 == val2:
        tp += 1
    elif val2 and val1 != val2:
        fp += 1
    elif not val2 and val1 != val2:
        fn += 1
    else:
        tn += 1
    total += 1

print('f1: {}'.format((2 * tp) / (2 * tp + fp + fn)))
print('acc: {}'.format((tp + tn) / total))
print('tpr: {}, tnr: {}, fpr: {}, fnr: {}'.format(tp / (tp + fp), tn / (tn + fn), fp / (tp + fp), fn / (tn + fn)))
