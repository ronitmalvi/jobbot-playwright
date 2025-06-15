def log_job(job, status):
    print(f"{status.upper()} | {job['title']} at {job['company']} | {job['link']}")