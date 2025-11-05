from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("<url>")
    print("Log in manually. The script will save state once you reach the inventory page.")
    input("Press Enter to check if logged in...")
    context.storage_state(path="test.json")
    print("Storage state saved.")
    browser.close()
