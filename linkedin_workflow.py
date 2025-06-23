from airtop import Browser
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD

def login_to_linkedin():
    browser = Browser(headless=False)
    page = browser.new_page()
    page.goto("https://www.linkedin.com/login")
    page.find("input#username").fill(LINKEDIN_EMAIL)
    page.find("input#password").fill(LINKEDIN_PASSWORD)
    page.find("button[type='submit']").click()
    page.wait_for_url("https://www.linkedin.com/feed/")
    return page