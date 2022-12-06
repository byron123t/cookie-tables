import os
import requests
import webbrowser
from bs4 import BeautifulSoup


counter = 0
skip = 2163
with open('actual_cookie_tables.csv', 'a') as outfile:
    for file in os.listdir('data/cookie_table/consolidated_urls/'):
        with open('data/cookie_table/consolidated_urls/{}'.format(file), 'r') as infile:
            for line in infile:
                url = line.strip()
    # for file in os.listdir('data/cookie_table/consolidated_html'):
                if skip > counter:
                    print(counter)
                    counter += 1
                    continue
                if 'policies.google.com/technologies/cookies' in url or 'aboutcookies.org/cookie-policy' in url or 'facebook.com/policies/cookies/' in url:
                    outfile.write('{},{}\n'.format(url, 1))
                    print(counter)
                    counter += 1
                    continue
                elif 'policies.google.com' in url or 'allaboutcookies.org' in url or 'support.google.com' in url or 'support.mozilla.org' in url or 'support.microsoft.com' in url or 'whatarecookies.com' in url:
                    outfile.write('{},{}\n'.format(url, 0))
                    print(counter)
                    counter += 1
                    continue
                elif 'aboutcookies.org' in url:
                    outfile.write('{},{}\n'.format(url, 2))
                    print(counter)
                    counter += 1
                    continue

                webbrowser.open(url)
                # key = file.replace('-|slash|-', '/')
                print(counter)
                annotation = input()
                if len(annotation) == 0:
                    annotation = 0
                outfile.write('{},{}\n'.format(url, annotation))
                counter += 1
                outfile.flush()
