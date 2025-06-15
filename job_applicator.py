from openai import OpenAI
import os
import time
from groq import Groq # Import the Groq client

# Initialize the Groq client
# Groq API key will be automatically loaded from the GROQ_API_KEY environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(label, resume): # Renamed function to reflect Groq usage
    prompt = f"""
Given the following resume:
---
{resume}
---

Please provide the appropriate value for the input field described as: "{label}".

Constraints:
- Respond ONLY with the requested value. Do NOT include any introductory or concluding sentences.
- The answer must match the expected data type for the field as described in the rules below.
- Prioritize information directly from the resume. If the information is not available and cannot be logically inferred, respond with "N/A".
- For date fields, use YYYY-MM-DD format.
- For Phone country code, use the format: [Country] ([country code]) (e.g.,India (+91)).
- For phone numbers, use the format: [number] (e.g., 9876543210), do not include country code.
- For email addresses, ensure it's a valid email format.
- For numeric fields, provide only the digits.
- For yes/no or boolean fields, respond with 'Yes' or 'No'.
- For fields asking for a list (e.g., skills), respond with a comma-separated list if applicable.
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192", # Or another Groq model, like "mixtral-8x7b-32768"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

# Example usage (assuming you have a resume string and a label)
# resume_text = "..."
# field_label = "Name"
# answer = ask_groq(field_label, resume_text)
# print(answer)

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def ask_openai(label, resume):
#     prompt = f"""
# Given the following resume:
# ---
# {resume}
# ---

# Please provide the appropriate value for the input field described as: "{label}".

# Constraints:
# - Respond ONLY with the requested value. Do NOT include any introductory or concluding sentences.
# - The answer must match the expected data type for the field as described in the rules below.
# - Prioritize information directly from the resume. If the information is not available and cannot be logically inferred, respond with "N/A".
# - For date fields, use YYYY-MM-DD format.
# - For phone numbers, use the format: [number] (e.g., 9876543210).
# - For email addresses, ensure it's a valid email format.
# - For numeric fields, provide only the digits.
# - For yes/no or boolean fields, respond with 'Yes' or 'No'.
# - For fields asking for a list (e.g., skills), respond with a comma-separated list if applicable.
# """
#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.2
#     )
#     return response.choices[0].message.content.strip()


def apply_to_current_job(page, resume_text: str):
    try:
        page.wait_for_selector(".jobs-apply-button", timeout=5000)
        apply_button = page.query_selector(".jobs-apply-button")
        if not apply_button or "Easy Apply" not in apply_button.inner_text():
            print("❌ Not an Easy Apply job")
            return False

        print("▶️ Clicking Easy Apply")
        apply_button.click()
        page.wait_for_selector(".jobs-easy-apply-modal", timeout=10000)

        form = page.query_selector(".jobs-easy-apply-modal")
        if not form:
            print("❌ Easy Apply modal not found.")
            return False

        while True:
            # INPUT, TEXTAREA, SELECT
            fields = form.query_selector_all("input:not([type='radio']):not([type='checkbox']), textarea, select")

            for field in fields:
                try:
                    label_text = ""
                    field_id = field.get_attribute("id")
                    if field_id:
                        label_el = form.query_selector(f"label[for='{field_id}']")
                        if label_el:
                            label_text = label_el.inner_text().strip()

                    if not label_text:
                        label_text = field.get_attribute("aria-label") or field.get_attribute("placeholder") or "Field"

                    print(f"📝 Label detected: {label_text}")
                    value = ask_groq(label_text, resume_text)
                    print(f"🤖 {label_text}: {value}")

                    tag_name = field.evaluate("node => node.tagName.toLowerCase()")
                    if tag_name == "select":
                        try:
                            field.select_option(label=value)
                            print(f"📥 Selected '{value}' in native dropdown")
                        except:
                            print(f"⚠️ Native select failed for '{label_text}', trying custom dropdown")
                            try:
                                # Custom LinkedIn dropdown workaround
                                field.click()  # opens the dropdown
                                time.sleep(0.5)

                                # Get all visible options (often rendered in a popup div elsewhere in the DOM)
                                dropdown_options = page.query_selector_all("li[role='option'], div[role='option']")

                                matched = False
                                for opt in dropdown_options:
                                    if value.lower() in opt.inner_text().strip().lower():
                                        opt.click()
                                        print(f"✅ Clicked custom dropdown option: {opt.inner_text().strip()}")
                                        matched = True
                                        break

                                if not matched:
                                    print(f"❌ Could not find dropdown option matching: {value}")
                            except Exception as ex:
                                print(f"❌ Error handling custom dropdown for {label_text}: {ex}")
                    else:
                        field.fill(value)
                        print(f"✍️ Filled '{value}'")
                    time.sleep(0.3)
                except Exception as e:
                    print(f"⚠️ Could not fill/select {label_text}\n{e}")

            # RADIO BUTTONS
            radios = form.query_selector_all("input[type='radio']")
            for radio in radios:
                try:
                    name = radio.get_attribute("name")
                    label_el = radio.evaluate_handle("r => r.closest('label')")
                    label_text = label_el.inner_text().strip() if label_el else name
                    if not label_text:
                        continue
                    answer = ask_groq(label_text, resume_text)
                    matching_labels = form.query_selector_all("label")
                    for label in matching_labels:
                        if answer.lower() in label.inner_text().lower():
                            label.click()
                            print(f"🔘 Selected radio: {label.inner_text().strip()}")
                            time.sleep(0.3)
                            break
                except Exception as e:
                    print(f"⚠️ Could not select radio button\n{e}")

            # BUTTON NAVIGATION
            review_btn = form.query_selector("button[aria-label='Review your application']:not([disabled])")
            next_btn = form.query_selector("button[aria-label='Continue to next step']:not([disabled])")
            submit_btn = form.query_selector("button[aria-label='Submit application']:not([disabled])")

            if review_btn:
                print("🔍 Clicking Review")
                review_btn.click()
                page.wait_for_timeout(2000)
                continue
            elif next_btn:
                print("➡️ Clicking Next")
                next_btn.click()
                page.wait_for_timeout(2000)
                continue
            elif submit_btn:
                print("✅ Clicking Submit Application")
                submit_btn.click()
                print("🎉 Application Submitted")
                return True

            print("❌ No navigation button found. Exiting.")
            return False

    except Exception as e:
        print(f"❌ Error in application process: {e}")
        return False