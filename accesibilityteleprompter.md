Teleprompter Script:

Slide 1:

“Let’s begin by reviewing the accessibility testing tools we explored and the challenges we encountered.

BrowserStack’s Bulk Run tool runs tests on static pages without browser interaction, making it impossible to load lazy elements dynamically. The report is generated based only on the initial DOM state, which limits comprehensive accessibility testing.

WAVE API, while widely used, operates similarly. It charges API credits per URL, and the generated JSON report lacks detailed accessibility error insights. Users must manually review errors on their website, making automation difficult. We also attempted to automate the WAVE Chrome extension using Playwright, but it wasn’t feasible.

Pa11y, a command-line tool, provides better flexibility with Puppeteer integration for real-time browser interactions. However, it offers limited customization and is based on the HTML_CodeSniffer project, which only supports WCAG 2.1—not the latest WCAG 2.2 standards.

Given these challenges, we needed a more advanced and flexible solution.”

Slide 2:

“This is where Axe-Core stands out as the ideal solution.

Axe-Core fully supports WCAG 2.2 AA, ensuring compliance with the latest accessibility guidelines. It generates comprehensive reports, detailing violations, suggested fixes, and exact element locators.

Its flexibility allows testing different WCAG parameters based on specific requirements, and it integrates seamlessly with tools like Selenium and Playwright for automated browser interactions.

Additionally, Axe-Core enables targeted testing of specific DOM elements, allowing us to focus on newly developed components instead of scanning entire pages.

It is highly scalable—capable of running tests across multiple URLs in parallel, making it ideal for large-scale audits. Moreover, its seamless integration into CI/CD pipelines ensures continuous accessibility validation throughout development.

For all these reasons, Axe-Core is the best tool for our accessibility automation framework.”
