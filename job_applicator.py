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


def apply_to_current_job(session, resume_text: str):
    try:
        session.wait_for_selector(".jobs-apply-button", timeout=5000)
        apply_button = session.query_selector(".jobs-apply-button")
        if not apply_button or "Easy Apply" not in session.get_text(apply_button):
            print("❌ Not an Easy Apply job")
            return False

        print("▶️ Clicking Easy Apply")
        session.click_element(apply_button)
        session.wait_for_selector(".jobs-easy-apply-modal", timeout=10000)

        form = session.query_selector(".jobs-easy-apply-modal")
        if not form:
            print("❌ Easy Apply modal not found.")
            return False

        while True:
            # INPUT, TEXTAREA, SELECT
            fields = session.query_selector_all("input:not([type='radio']):not([type='checkbox']), textarea, select", parent=form)

            for field in fields:
                try:
                    label_text = ""
                    field_id = session.get_attribute(field, "id")
                    if field_id:
                        label_el = session.query_selector(f"label[for='{field_id}']", parent=form)
                        if label_el:
                            label_text = session.get_text(label_el).strip()

                    if not label_text:
                        label_text = (session.get_attribute(field, "aria-label") or 
                                    session.get_attribute(field, "placeholder") or "Field")

                    print(f"📝 Label detected: {label_text}")
                    value = ask_groq(label_text, resume_text)
                    print(f"🤖 {label_text}: {value}")

                    tag_name = session.get_tag_name(field)
                    if tag_name.lower() == "select":
                        try:
                            session.select_option(field, value)
                            print(f"📥 Selected '{value}' in native dropdown")
                        except:
                            print(f"⚠️ Native select failed for '{label_text}', trying custom dropdown")
                            try:
                                # Custom LinkedIn dropdown workaround
                                session.click_element(field)  # opens the dropdown
                                time.sleep(0.5)

                                # Get all visible options (often rendered in a popup div elsewhere in the DOM)
                                dropdown_options = session.query_selector_all("li[role='option'], div[role='option']")

                                matched = False
                                for opt in dropdown_options:
                                    if value.lower() in session.get_text(opt).strip().lower():
                                        session.click_element(opt)
                                        print(f"✅ Clicked custom dropdown option: {session.get_text(opt).strip()}")
                                        matched = True
                                        break

                                if not matched:
                                    print(f"❌ Could not find dropdown option matching: {value}")
                            except Exception as ex:
                                print(f"❌ Error handling custom dropdown for {label_text}: {ex}")
                    else:
                        session.type_text(field, value, clear=True)
                        print(f"✍️ Filled '{value}'")
                    time.sleep(0.3)
                except Exception as e:
                    print(f"⚠️ Could not fill/select {label_text}\n{e}")

            # RADIO BUTTONS
            radios = session.query_selector_all("input[type='radio']", parent=form)
            for radio in radios:
                try:
                    name = session.get_attribute(radio, "name")
                    # Find the closest label for this radio button
                    label_el = session.execute_script(f"""
                        const radio = arguments[0];
                        return radio.closest('label') || document.querySelector('label[for="' + radio.id + '"]');
                    """, radio)
                    label_text = session.get_text(label_el).strip() if label_el else name
                    if not label_text:
                        continue
                    answer = ask_groq(label_text, resume_text)
                    matching_labels = session.query_selector_all("label", parent=form)
                    for label in matching_labels:
                        if answer.lower() in session.get_text(label).lower():
                            session.click_element(label)
                            print(f"🔘 Selected radio: {session.get_text(label).strip()}")
                            time.sleep(0.3)
                            break
                except Exception as e:
                    print(f"⚠️ Could not select radio button\n{e}")

            # BUTTON NAVIGATION
            review_btn = session.query_selector("button[aria-label='Review your application']:not([disabled])", parent=form)
            next_btn = session.query_selector("button[aria-label='Continue to next step']:not([disabled])", parent=form)
            submit_btn = session.query_selector("button[aria-label='Submit application']:not([disabled])", parent=form)

            if review_btn:
                print("🔍 Clicking Review")
                session.click_element(review_btn)
                session.wait(2000)
                continue
            elif next_btn:
                print("➡️ Clicking Next")
                session.click_element(next_btn)
                session.wait(2000)
                continue
            elif submit_btn:
                print("✅ Clicking Submit Application")
                session.click_element(submit_btn)
                print("🎉 Application Submitted")
                return True

            print("❌ No navigation button found. Exiting.")
            return False

    except Exception as e:
        print(f"❌ Error in application process: {e}")
        return False