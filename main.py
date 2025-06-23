from resume_parser import parse_resume
from linkedin_auth import login_to_linkedin
from job_search import get_job_cards
from gpt_relevance_checker import is_relevant
from job_applicator import apply_to_current_job
from logger import log_job
import time

MAX_APPLICATIONS = 10
ROLE = "Software Engineer Easy Apply"

print("🚀 Starting LinkedIn Job Application Bot with Airtop AI")
print("📄 Parsing resume...")
resume_text = parse_resume("resume.pdf")

print("🔐 Logging into LinkedIn...")
session_info = login_to_linkedin("dewa.ai2050@gmail.com", "Dewa@AI2050")

# Extract session components
airtop_client = session_info['client']
session_id = session_info['session_id']
window_id = session_info['window_id']

print("🔍 Navigating to LinkedIn Jobs...")
# Navigate to LinkedIn Jobs page
jobs_window = airtop_client.windows.create(
    session_id=session_id,
    url="https://www.linkedin.com/jobs"
)

print("⏳ Waiting for page to load...")
time.sleep(5)

print("📝 Searching for jobs...")
print(f"🎯 Role: {ROLE}")
print(f"📊 Max applications: {MAX_APPLICATIONS}")

print("⚠️  IMPORTANT: This version requires manual interaction with the Airtop browser.")
print("   1. Go to your Airtop dashboard: https://portal.airtop.ai/")
print("   2. Find your active session and open it")
print("   3. Manually search for jobs and apply")
print("   4. The automation will be enhanced in the next version")

# Keep session alive for manual interaction
print("🕐 Keeping session alive for 30 minutes...")
for i in range(30):  # 30 minutes
    print(f"⏳ Session active... {30-i} minutes remaining")
    time.sleep(60)  # Wait 1 minute

# Close session
try:
    airtop_client.sessions.terminate(session_id)
    print("✅ Session terminated successfully")
except:
    print("⚠️ Session may have already expired")

print("🎯 Job application session completed!")