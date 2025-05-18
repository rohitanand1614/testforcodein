# Step 1: Get and save cookies
driver.get("https://your-form-page.com")
time.sleep(5)  # wait for Munchkin cookie to be set

cookies = driver.get_cookies()  # save cookies to a variable or file

# Step 2: For each entry
for entry in entries_list:
    driver.delete_all_cookies()
    driver.get("https://your-form-page.com")
    
    # Add saved cookies back
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    driver.refresh()  # reload page with cookies set
    
    # Now fill form and submit with slow typing etc.
    # slow_type(driver.find_element(...), entry["email"])
    # ...
import time
import random
from selenium.webdriver.common.action_chains import ActionChains

def slow_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))  # random delay between 100-300 ms

# Example usage:
input_field = driver.find_element_by_id("form_field_id")
input_field.click()

# Simulate mouse move over input (optional)
actions = ActionChains(driver)
actions.move_to_element(input_field).perform()

slow_type(input_field, "test@example.com")



driver.execute_script("arguments[0].focus();", input_field)
slow_type(input_field, "rohit@example.com")
driver.execute_script("arguments[0].blur();", input_field)


driver.execute_script("arguments[0].focus();", input_field)
slow_type(input_field, "rohit@example.com")
input_field.send_keys(Keys.TAB) 
