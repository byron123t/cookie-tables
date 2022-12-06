import os
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


MUTED=["#4878D0", "#EE854A", "#6ACC64", "#D65F5F", "#956CB4", "#8C613C", "#DC7EC0", "#797979", "#D5BB67", "#82C6E2"]
PAL = sns.color_palette(MUTED)

classes = []
with open('data/cookie_table/confusion_matrix.txt', 'r') as infile:
    for i, line in enumerate(infile):
        classes.append([])
        split = line.replace('[', '').replace(']', '').strip().split()
        for item in split:
            classes[i].append(int(item))

sns.set(font_scale=4, style='ticks')
plt.figure(figsize=(16, 12))
g = sns.heatmap(classes, cbar=True, cmap='Blues')
plt.tight_layout()
sns.despine()
plt.savefig('data/plots/confusion_matrix.pdf')
