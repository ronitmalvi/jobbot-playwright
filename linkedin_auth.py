# linkedin_auth.py
from playwright.sync_api import sync_playwright
import time

def login_to_linkedin(email, password):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.linkedin.com/login")
    page.fill("input#username", email)
    page.fill("input#password", password)
    page.click("button[type='submit']")

    print("⏳ Please complete any security check manually...")
    page.wait_for_timeout(10000)  # Wait 10 seconds for manual puzzle solve

    return page, browser, playwright
