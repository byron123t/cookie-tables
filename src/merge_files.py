import os


urls = {}
for file in os.listdir('data/cookie_table/potential_pages/'):
    file1 = open(os.path.join('data/cookie_table/potential_pages/', file), 'r')
    for line in file1:
        url = line.strip()
        if file in urls and url not in urls[file]:
            urls[file].append(url)
        else:
            urls[file] = [url]

for file in os.listdir('data/cookie_table/backup/potential_pages/'):
    file1 = open(os.path.join('data/cookie_table/backup/potential_pages/', file), 'r')
    for line in file1:
        url = line.strip()
        if file in urls and url not in urls[file]:
            urls[file].append(url)
        else:
            urls[file] = [url]

for file in os.listdir('data/cookie_table/backup2/potential_pages/'):
    file1 = open(os.path.join('data/cookie_table/backup2/potential_pages/', file), 'r')
    for line in file1:
        url = line.strip()
        if file in urls and url not in urls[file]:
            urls[file].append(url)
        else:
            urls[file] = [url]

for file, urls in urls.items():
    with open('data/cookie_table/consolidated_urls/{}'.format(file), 'w') as outfile:
        for url in urls:
            outfile.write('{}\n'.format(url))
