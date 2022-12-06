import os
from bs4 import BeautifulSoup


with open('data/cookie_table/all_urls.csv', 'r') as infile:
    for line in infile:
        split = line.strip().split(',')
        label = split[0]
        url = split[1]
        if label != 'nothing' and label != 'false_positive':
            if os.path.exists('data/cookie_table/consolidated_html/{}.html'.format(url.replace('/', '-|slash|-'))):
                with open('data/cookie_table/consolidated_html/{}.html'.format(url.replace('/', '-|slash|-')), 'r') as htmldoc:
                    html_doc = htmldoc.read()
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    with open('data/cookie_table/consolidated_plaintext/{}.txt'.format(url.replace('/', '-|slash|-')), 'w') as outfile:
                        outfile.write(soup.get_text())
