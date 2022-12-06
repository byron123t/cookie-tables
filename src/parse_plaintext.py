import os
import re
from tqdm import tqdm


for file in tqdm(os.listdir('data/cookie_table/consolidated_plaintext')):
    with open(os.path.join('data/cookie_table/consolidated_plaintext', file), 'r') as infile:
        sentences = []
        for line in infile:
            stripped = line.strip()
            if len(stripped) > 0:
                sentences.extend(re.split('\.\s+|;\s+', stripped))
        with open(os.path.join('data/cookie_table/consolidated_sentences', file), 'w') as outfile:
            for i, sentence in enumerate(sentences):
                outfile.write('{}\n'.format(sentence))
        with open(os.path.join('data/cookie_table/consolidated_labels', file), 'w') as outfile:
            pass
