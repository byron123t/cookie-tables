import os


everything_dict = {'nothing': [], 'cookie_declaration': [], 'cookie_settings': [], 'other': [], 'entities': [], 'purposes': [], 'activities': [], 'false_positive': []}

with open('data/cookie_table/actual_cookie_tables.csv', 'r') as infile:
    for line in infile:
        split = line.strip().split(',')
        url = split[0]
        if '0' in split[1]:
            if url not in everything_dict['nothing']:
                everything_dict['nothing'].append(url)
        if '1' in split[1]:
            if url not in everything_dict['cookie_declaration']:
                everything_dict['cookie_declaration'].append(url)
        if '2' in split[1]:
            if url not in everything_dict['cookie_settings']:
                everything_dict['cookie_settings'].append(url)
        if '3' in split[1]:
            if url not in everything_dict['other']:
                everything_dict['other'].append(url)
        if '4' in split[1]:
            if url not in everything_dict['entities']:
                everything_dict['entities'].append(url)
        if '5' in split[1]:
            if url not in everything_dict['purposes']:
                everything_dict['purposes'].append(url)
        if '6' in split[1]:
            if url not in everything_dict['activities']:
                everything_dict['activities'].append(url)
        if '7' in split[1]:
            if url not in everything_dict['false_positive']:
                everything_dict['false_positive'].append(url)
        if 'http' in split[1]:
            if url not in everything_dict['cookie_declaration']:
                everything_dict['cookie_declaration'].append(url)
    with open('data/cookie_table/parsed_annotations.csv', 'w') as outfile:
        for key, val in everything_dict.items():
            outfile.write('{},{}\n'.format(key, len(val)))
    with open('data/cookie_table/all_urls.csv', 'w') as outfile:
        for key, val in everything_dict.items():
            for item in val:
                outfile.write('{},{}\n'.format(key, item))
