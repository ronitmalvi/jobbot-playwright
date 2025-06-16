import groq
from gpt_client import ask_groq

def fill_easy_apply(page, resume_text):
    """
    Fills out an "Easy Apply" job application form on LinkedIn using Groq to
    generate answers based on a provided resume text.

    Args:
        page (playwright.sync_api.Page): The Playwright page object of the application modal.
        resume_text (str): The text content of the user's resume.

    Returns:
        bool: True if navigation buttons are found and clicked, False otherwise.
    """
    modal = page.find(".jobs-easy-apply-modal")
    for field_el in modal.find_all("input, textarea, select"):
        if not field_el.visible:
            continue

        lid = field_el.get_attribute("id") or ""
        label_text = ""
        if lid:
            label_el = modal.find(f"label[for='{lid}']")
            if label_el:
                label_text = label_el.text.strip()
        if not label_text:
            label_text = field_el.get_attribute("aria-label") or field_el.get_attribute("placeholder") or "Field"

        # Use ask_groq instead of ask_openai
        answer = ask_groq(f"Label: {label_text}\nResume:\n{resume_text}")
        print(f"\u2192 Filling {label_text} with {answer}")

        tag = field_el.tag_name
        if tag == "select":
            try:
                field_el.select_option(label=answer)
            except: # Fallback for select elements that don't respond to select_option
                field_el.click()
                for opt in page.find_all("li[role=option]"):
                    if answer.lower() in opt.text.strip().lower():
                        opt.click()
                        break
        else:
            field_el.fill(answer)

    for btn_text in ["Continue to next step", "Review your application", "Submit application"]:
        btn = modal.find(f"button:has-text('{btn_text}')")
        if btn:
            print(f"\ud83d\udd01 Clicking '{btn_text}'")
            btn.click()
            return btn_text != "Submit application"
    print("\ud83d\udeab No navigation button found")
    return False