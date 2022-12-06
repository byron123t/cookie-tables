import os
import requests
import webbrowser
from bs4 import BeautifulSoup


counter = 0
skip = 2167
with open('data/cookie_table/actual_cookie_tables.csv', 'a') as outfile:
    for file in os.listdir('data/cookie_table/consolidated_urls/'):
        with open('data/cookie_table/consolidated_urls/{}'.format(file), 'r') as infile:
            for line in infile:
                url = line.strip()
                if skip > counter:
                    print(counter)
                    counter += 1
                    continue
                webbrowser.open(url)
                print(counter)
                annotation = input()
                outfile.write('{},{}\n'.format(url, annotation))
                counter += 1
