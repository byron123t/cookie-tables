import re
import os
import argparse
import pandas as pd
from playwright.sync_api import Page, expect, sync_playwright
from src.perceptor.html.parse_html import ParseHtml


def recurse_urls(page, tag, url, depth):
    if depth > 2:
        return False
    try:
        if tag.get_attribute('href') in VISITED_URLS or tag.get_attribute('href').split('#')[0] in VISITED_URLS:
            return False
    except Exception as e:
        pass
    # with page.expect_navigation():
    # print(tag)
    # print(page.url)
    try:
        tag.click(button='left', force=True)
    except Exception as e:
        try:
            tag.click(button='left', force=True)
        except Exception as e:
            return False
    try:
        page.wait_for_load_state('networkidle')
    except Exception as e:
        try:
            page.wait_for_load_state('domcontentloaded')
        except Exception as e:
            return False
    if page.url in VISITED_URLS or page.url.split('#')[0] in VISITED_URLS:
        return False
    if '#' in page.url:
        VISITED_URLS.append(page.url.split('#')[0])
    else:
        VISITED_URLS.append(page.url)

    html = page.content()
    parser = ParseHtml(html=html)
    text = parser.get_page_text()
    tables = len(parser.get_tables())
    if page.url not in POTENTIAL_PAGES or page.url.split('#')[0] not in POTENTIAL_PAGES:
        if tables > 0 and ('cookie-table' in page.url or 'cookie_table' in page.url or 'cookietable' in page.url or 'cookie-list' in page.url or 'cookielist' in page.url or 'cookie_list' in page.url):
            with open('data/cookie_table/definite_pages/{}.txt'.format(url), 'w') as outfile:
                outfile.write(page.url)
            return True
        elif ('cookie table' in text or 'cookie_table' in text or 'cookie-table' in text or 'cookie list' in text or 'cookie_list' in text or 'cookie-list' in text or 'table of cookies' in text or 'table of our cookies' in text or 'list of cookies' in text or 'list of our cookies' in text) or (tables > 0 and ('cookies' in page.url or 'cookie-statement' in page.url or 'cookie-policy' in page.url or 'cookiestatement' in page.url or 'cookiepolicy' in page.url or 'cookie_statement' in page.url or 'cookie_policy' in page.url) and ('cookie' in text) and ('expires' in text or 'retention' in text or 'expiration' in text) and ('purpose' in text or 'description' in text or 'category' in text or 'categories' in text) and ('cookie name' in text) and ('party' in text)) or ('cookies' in page.url or 'cookie-statement' in page.url or 'cookie-policy' in page.url or 'cookiestatement' in page.url or 'cookiepolicy' in page.url or 'cookie_statement' in page.url or 'cookie_policy' in page.url or ('cookie' in text and (('expir' in text or 'retention' in text) and ('purpose' in text or 'description' in text or 'categor' in text)))):
            if '#' in page.url:
                POTENTIAL_PAGES.append(page.url.split('#')[0])
            else:
                POTENTIAL_PAGES.append(page.url)
            with open('data/cookie_table/potential_pages/{}.txt'.format(url), 'a') as outfile:
                outfile.write('{}\n'.format(page.url))

    interactables = []
    interactables.append(page.locator('button:has-text("{}")'.format('cookie table')))
    interactables.append(page.locator('a:has-text("{}")'.format('cookie table')))
    interactables.append(page.locator('a >> a[href*="{}"]'.format('cookie-table')))
    interactables.append(page.locator('a >> a[href*="{}"]'.format('cookietable')))
    interactables.append(page.locator('a >> a[href*="{}"]'.format('cookie_table')))
    interactables.append(page.locator('button:has-text("{}")'.format('cookie')))
    interactables.append(page.locator('a:has-text("{}")'.format('cookie')))
    interactables.append(page.locator('a >> a[href*="{}"]'.format('cookie')))

    for newtag in interactables:
        for i in range(newtag.count()):
            found = recurse_urls(page, newtag.nth(i), url, depth + 1)
            if found:
                return True
    return False


def test_playwright(playwright, file):
    global VISITED_URLS
    global POTENTIAL_PAGES
    chromium = playwright.chromium
    browser = chromium.launch()
    context = browser.new_context(
        # record_video_dir="data/cookie_table/videos/",
        # record_video_size={"width": 640, "height": 480}
    )
    context.set_default_timeout(5000)
    page = context.new_page()
    count = 0
    with open('data/cookie_table/tranco/{}.csv'.format(file), 'r') as infile:
        for line in infile:
            count += 1
            found = False
            url = line.strip()
            try:
                page.goto('https://{}'.format(url))
                page.wait_for_load_state('domcontentloaded')
            except Exception as e:
                try:
                    page.goto('https://{}'.format(url))
                    page.wait_for_load_state('domcontentloaded')
                except Exception as e:
                    try:
                        page.wait_for_load_state('domcontentloaded')
                    except Exception as e:
                        continue
            interactables = []

            VISITED_URLS = [url]
            POTENTIAL_PAGES = []

            interactables.append(page.locator('button:has-text("{}")'.format('cookie table')))
            interactables.append(page.locator('a:has-text("{}")'.format('cookie table')))
            interactables.append(page.locator('a >> [href*="{}"]'.format('cookie-table')))
            interactables.append(page.locator('a >> a[href*="{}"]'.format('cookietable')))
            interactables.append(page.locator('a >> a[href*="{}"]'.format('cookie_table')))

            interactables.append(page.locator('button:has-text("{}")'.format('cookie')))
            interactables.append(page.locator('a:has-text("{}")'.format('cookie')))
            interactables.append(page.locator('a >> a[href*="{}"]'.format('cookie')))

            interactables.append(page.locator('button:has-text("{}")'.format('privacy')))
            interactables.append(page.locator('a:has-text("{}")'.format('privacy')))
            interactables.append(page.locator('a >> a[href*="{}"]'.format('privacy')))
            try:
                for tag in interactables:
                    for i in range(tag.count()):
                        found = recurse_urls(page, tag.nth(i), url, 0)
                    if found:
                        break
            except Exception as e:
                continue
            with open('data/cookie_table/visited_urls.csv', 'a') as outfile:
                outfile.write('{}\n'.format(url))
