import time
from playwright.sync_api import Page

def get_job_cards(page: Page):
    # Wait until job list is present
    page.wait_for_selector("main ul", timeout=10000)

    # Select all job cards (li elements inside the ul)
    job_elements = page.query_selector_all("main ul")

    # Remove duplicates by their inner_text or href (if available)
    unique_jobs = []
    seen = set()
    for job in job_elements:
        identifier = job.inner_text().strip()
        if identifier not in seen:
            seen.add(identifier)
            unique_jobs.append(job)

    print(f"✅ Found {len(unique_jobs)} unique jobs.")
    return unique_jobs
