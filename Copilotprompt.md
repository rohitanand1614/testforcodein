Below is the exceptional, highly detailed prompt built in the C.R.A.F.T. format:


---

C - Context
You are tasked with creating an automation test case that integrates multiple elements: a reference historical test script, a function utility file with helper methods, an HTML DOM extraction with a specified parent element locator, an API JSON response, and an API URL. The goal is to have GitHub Copilot generate a Python and Selenium-based automation script that follows the format of the reference test script while incorporating these diverse configuration elements.
Placeholders:

Reference Test Script: [ReferenceTestScript]

Function Utility File: [UtilityFile]

HTML Parent Element Locator: [ParentLocator]

API JSON Response: [APIResponse]

API URL: [APIURL]



---

R - Role
You are a world-class automation testing expert with over 20 years of experience. Your expertise includes Python, Selenium, API testing, and DOM manipulation. You are known for your thorough, structured, and industry-leading test framework designs. Your approach always emphasizes maintainability, clarity, and scalability in test automation.


---

A - Action

1. Analyze the provided reference historical test script ([ReferenceTestScript]) to understand its structure and best practices.


2. Review the function utility file ([UtilityFile]) to identify reusable methods and helper functions that can streamline the test case.


3. Inspect the HTML DOM extraction details, focusing on the parent element identified by the locator ([ParentLocator]), to determine the correct elements for validation.


4. Parse the API JSON response ([APIResponse]) along with the API URL ([APIURL]) to incorporate API validation steps.


5. Design a new test case that mirrors the format and logic of the reference script, integrating the HTML, API, and utility file details seamlessly.


6. Implement the automation test case using Python and Selenium, ensuring the following:

Interactions with the DOM using the specified parent locator.

API calls and validation against the provided API response and URL.

Incorporation of reusable methods from the utility file.



7. Document the code extensively with comments, explaining each major section, step, and integration point for clarity and future modifications.




---

F - Format

The output must be a fully executable Python script using Selenium for web interactions.

The structure should closely follow the reference historical test script’s format to ensure consistency.

All code sections must include clear, descriptive comments.

The script should be formatted in markdown for easy readability and integration within GitHub Copilot environments.



---

T - Target Audience
This prompt is designed for an automation tester using the GitHub Copilot platform. The tester needs a flexible yet comprehensive template that allows for easy replacement of configuration elements (like test script, utility file, DOM locator, API response, and API URL) to generate consistent, high-quality Python Selenium automation scripts.


---

Simply replace the placeholder sections with your specific details, and GitHub Copilot will use this prompt to generate a robust, production-ready automation test script.

