from resume_parser import parse_resume
from linkedin_workflow import login_to_linkedin
from job_applicator import fill_easy_apply
from config import ROLE, MAX_APPLICATIONS
import time

def main():
    resume_text = parse_resume("resume.pdf")
    page = login_to_linkedin()
    page.goto("https://www.linkedin.com/jobs")
    page.wait_for_selector("input[aria-label='Search by title, skill, or company']").fill(ROLE)
    page.find("input[aria-label='Search by title, skill, or company']").press("Enter")
    page.wait_for_selector("ul.jobs-search__results-list li")

    applied = 0
    job_cards = page.find_all("ul.jobs-search__results-list li")
    for job in job_cards:
        job.click()
        time.sleep(2)
        btn = page.find(".jobs-apply-button")
        if btn and "Easy Apply" in btn.text:
            btn.click()
            time.sleep(2)
            should_continue = True
            while should_continue:
                should_continue = fill_easy_apply(page, resume_text)
            applied += 1
            print(f"\u2705 Applied to job #%d" % applied)
            if applied >= MAX_APPLICATIONS:
                break

if __name__ == "__main__":
    main()