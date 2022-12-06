from playwright.sync_api import Page, expect, sync_playwright
from scrape_pages import test_playwright


for i in range(420, 440):
    with sync_playwright() as playwright:
        print(i)
        test_playwright(playwright, i)
