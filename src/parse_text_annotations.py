import os
import csv
import random


labels = {}
sentences = []
outlabels = []

with open('data/cookie_table/comprehensive_annotations.csv', 'w') as outfile:
    for file in os.listdir('data/cookie_table/consolidated_labels'):
        with open(os.path.join('data/cookie_table/consolidated_labels', file), 'r') as infile:
            with open(os.path.join('data/cookie_table/consolidated_sentences', file), 'r') as sentence_file:
                temp_sentences = []
                for sentence in sentence_file:
                    temp_sentences.append(sentence.strip())
                for i, line in enumerate(infile):
                    split = line.strip().split(',')
                    for item in split:
                        if len(item) > 0:
                            if item not in labels:
                                labels[item] = 0
                            labels[item] += 1
                    if len(split[0]) > 0:
                        outlabels.append(split)
                        sentences.append(temp_sentences[i])

    indices = []
    for i in range(len(sentences)):
        indices.append(i)
    random.shuffle(indices)
    writer = csv.writer(outfile, delimiter='|')
    for i in indices:
        writer.writerow([sentences[i], outlabels[i]])

num_sentences = 0
print(labels)
for key, val in labels.items():
    num_sentences += val
print(num_sentences)
