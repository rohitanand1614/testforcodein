Act as a test automation expert in Python and Playwright and help me design an automation script with the following functionalities:

Test Data Preparation:

I will provide the test data as a JSON-styled Excel sheet containing URLs and corresponding language prefixes.
For each row, construct URLs for each language by replacing “.com/” in the English URL with “.com/<lang-code>/”, using prefixes separated by commas from the sheet.
Automation Steps and Execution:

Load the English page using Python and Playwright, scroll slowly to allow lazy loading of the content, and capture all visible text from the body.
Count occurrences of non-translatable text (from a separate Excel sheet) within this captured English text.
Repeat the above process for two other language-specific pages and count the same non-translatable text occurrences.
Data Collection and Parallel Execution:

Create results with columns: test URL, non-translatable text, count on English page, count on language-specific page, and match status.
Execute tests in parallel for each row of the test sheet containing URL and language codes.
Results Compilation:

Collate results from all executions and output them to an Excel sheet for review.
Please ensure the script handles exceptions and errors elegantly and optimize for performance during parallel execution.
</lang-code>
