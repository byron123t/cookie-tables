import os
from playwright.sync_api import Page, expect, sync_playwright


def check_and_write(url, tries=0, max_tries=9):
    if tries > max_tries:
        return False
    try:
        page.goto(url)
        page.wait_for_load_state('domcontentloaded')
        html = page.content()
        with open('data/cookie_table/consolidated_html/{}.html'.format(url.replace('/', '-|slash|-')), 'w') as outfile:
            outfile.write(html)
            return True
    except Exception as e:
        print(e)
        return check_and_write(url, tries + 1)


with sync_playwright() as playwright:
    chromium = playwright.chromium
    browser = chromium.launch()
    context = browser.new_context()
    context.set_default_timeout(5000)
    page = context.new_page()
    everything_dict = {'nothing': [], 'cookie_declaration': [], 'cookie_settings': [], 'other': [], 'entities': [], 'purposes': [], 'activities': [], 'false_positive': []}

    with open('data/cookie_table/actual_cookie_tables.csv', 'r') as infile:
        for line in infile:
            split = line.strip().split(',')
            url = split[0]
            store = False
            if '0' in split[1]:
                if url not in everything_dict['nothing']:
                    everything_dict['nothing'].append(url)
            if '1' in split[1]:
                if url not in everything_dict['cookie_declaration']:
                    everything_dict['cookie_declaration'].append(url)
                    store = True
            if '2' in split[1]:
                if url not in everything_dict['cookie_settings']:
                    everything_dict['cookie_settings'].append(url)
                    store = True
            if '3' in split[1]:
                if url not in everything_dict['other']:
                    everything_dict['other'].append(url)
                    store = True
            if '4' in split[1]:
                if url not in everything_dict['entities']:
                    everything_dict['entities'].append(url)
                    store = True
            if '5' in split[1]:
                if url not in everything_dict['purposes']:
                    everything_dict['purposes'].append(url)
                    store = True
            if '6' in split[1]:
                if url not in everything_dict['activities']:
                    everything_dict['activities'].append(url)
                    store = True
            if '7' in split[1]:
                if url not in everything_dict['false_positive']:
                    everything_dict['false_positive'].append(url)
            if store:
                if check_and_write(url):
                    print('Passed')
                else:
                    print('Failed')
        with open('data/cookie_table/parsed_annotations.csv', 'w') as outfile:
            for key, val in everything_dict.items():
                outfile.write('{},{}\n'.format(key, len(val)))
