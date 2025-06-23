import time

def get_job_cards(session):
    # Wait until job list is present
    session.wait_for_selector("main ul", timeout=10000)

    # Select all job cards (li elements inside the ul)
    job_elements = session.query_selector_all("main ul li")

    # Remove duplicates by their inner_text
    unique_jobs = []
    seen = set()
    for job in job_elements:
        identifier = session.get_text(job).strip()
        if identifier not in seen and identifier:
            seen.add(identifier)
            unique_jobs.append(job)

    print(f"✅ Found {len(unique_jobs)} unique jobs.")
    return unique_jobs