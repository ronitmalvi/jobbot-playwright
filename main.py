from resume_parser import parse_resume
from linkedin_auth import login_to_linkedin
from job_search import get_job_cards
from gpt_relevance_checker import is_relevant
from job_applicator import apply_to_current_job
from logger import log_job
import time

MAX_APPLICATIONS = 10
ROLE = "Software Engineer Easy Apply"

resume_text = parse_resume("resume.pdf")
page, browser, playwright = login_to_linkedin("dewa.ai2050@gmail.com", "Dewa@AI2050")

# Navigate to LinkedIn Jobs page
page.goto("https://www.linkedin.com/jobs")

# Wait until redirected to jobs page
while not page.url.startswith("https://www.linkedin.com/jobs"):
    print("Waiting for LinkedIn Jobs page to load...")
    time.sleep(2)

# Use targeted wait instead of networkidle
try:
    page.wait_for_selector("input[aria-label='Search by title, skill, or company']", timeout=15000)
except:
    print("⚠️ Could not find job search input field.")

time.sleep(3)



# Now try to get the search input reliably
search_input = None
for _ in range(5):
    try:
        search_input = page.wait_for_selector("input[aria-label='Search by title, skill, or company']", timeout=5000)
        if search_input:
            break
    except:
        print("Retrying to find search input...")
        time.sleep(2)

if not search_input:
    raise Exception("Search input not found. Check if page is loaded or blocked by LinkedIn security.")


page.wait_for_timeout(5000)

# Enter the job role
search_input = page.wait_for_selector("input[aria-label='Search by title, skill, or company']")
search_input.fill(ROLE)
search_input.press("Enter")
page.wait_for_timeout(5000)

applied = 0

while applied < MAX_APPLICATIONS:
    job_cards = get_job_cards(page)
    if not job_cards:
        print("🔄 No job cards found. Scrolling and retrying...")
        page.mouse.wheel(0, 1000)
        time.sleep(2)
        job_cards = get_job_cards(page)
        if not job_cards:
            print("❌ Still no job cards. Exiting.")
            break

    for job in job_cards:
        try:
            job.click()
            page.wait_for_timeout(3000)
            job_desc_el = page.query_selector('''.jobs-box__html-content
              RdfAIERUrxMgqhSEqErqXGPsRHOdmbuARcl
              t-14 t-normal
              jobs-description-content__text--stretch''')
            job_desc = job_desc_el.inner_text() if job_desc_el else ""
            # if is_relevant(job_desc, resume_text):
            #     if apply_to_current_job(page, resume_text):
            #         applied += 1
            #         print(f"✅ Applied to job ({applied}/{MAX_APPLICATIONS})")
            #     else:
            #         print("❌ Failed to apply")
            # else:
            #     print("⏭️ Skipped irrelevant job")
            if apply_to_current_job(page, resume_text):
                applied += 1
                print(f"✅ Applied to job ({applied}/{MAX_APPLICATIONS})")
            else:
                print("❌ Failed to apply")
            if applied >= MAX_APPLICATIONS:
                break
        except Exception as e:
            print(f"⚠️ Error processing job: {e}")
            continue

browser.close()
playwright.stop()