Based on the search results, there is no direct evidence that **Pa11y** currently supports **WCAG 2.2 AA**. Here’s a summary of the relevant findings:

1. **WCAG 2.2 Support Inquiry**: A GitHub issue from May 2023 explicitly asks whether Pa11y will be upgraded to support WCAG 2.2 or if it already does. However, there is no clear response or confirmation in the search results indicating that WCAG 2.2 is supported .

2. **WCAG 2.1 Support**: Pa11y has been inquired about supporting WCAG 2.1 in the past, and while there are discussions, the search results do not provide a definitive answer about full support for WCAG 2.1 AA, let alone WCAG 2.2 AA .

3. **Current Standards Supported**: Pa11y’s documentation and usage examples primarily mention support for **WCAG 2.0 A/AA/AAA** and **Section 508**. There is no mention of WCAG 2.2 in the official documentation or recent updates .

4. **Future Updates**: Some discussions hint at the possibility of future updates to support newer standards like WCAG 2.1 and potentially WCAG 2.2, but no concrete timelines or plans are provided .

### Conclusion
As of **February 2025**, Pa11y does not appear to support **WCAG 2.2 AA** based on the available information. If you require WCAG 2.2 compliance, you may need to explore alternative tools or wait for future updates from the Pa11y team. For the latest updates, you can monitor the [Pa11y GitHub repository](https://github.com/pa11y/pa11y) or their official website .


Pa11y supports multiple accessibility testing standards, including WCAG 2.0 AA and Section 508[7]. Pa11y relies on the axe and HTML_Codesniffer rules engines for test criteria, so support for WCAG 2.2 depends on those engines, as well as the Pa11y team's bandwidth[1].

As of May 2023, HTML_CS did not yet support WCAG 2.2, but axe core version 4.5 did. The Pa11y team was using an older version of axe at that time, but there was a chance that Pa11y might add support via axe before HTML_CS[1].

To stay up-to-date on the latest changes, the Pa11y team suggests keeping an eye on the Changelog[1].

Citations:
[1] https://github.com/pa11y/pa11y-ci/issues/205
[2] https://mikemadison.net/blog/2020/11/19/introduction-to-accessibility-testing-pa11y
[3] https://sparkbox.com/foundry/pa11y_website_accessibility_audit_website_accessibility_checker
[4] https://apostrophecms.com/accessibility
[5] https://www.w3.org/TR/WCAG22/
[6] https://s41911.pcdn.co/wp-content/uploads/uConnect-VCC-VPAT-2.5-WCAG-2.2-AA-2024-08.pdf
[7] https://rapidforms.co/blog/22-web-accessibility-testing-tools-for-forms-2024/
[8] https://www.accessibilitychecker.org/blog/top-five-accessibility-checkers/
[9] https://ckeditor.com/blog/automated-accessibility-testing/


This document explains how the open-source accessibility testing tool Pa11y can be used to support WCAG 2.2 AA compliance. Pa11y is a Node.js command-line interface that runs web pages against a set of accessibility rules. WCAG 2.2 AA are guidelines developed by the W3C to make web content more accessible to people with disabilities.
Pa11y was created to address the need for better tooling and automation in web accessibility and includes a web-based dashboard and CI/CD integration.
WCAG 2.2 AA is the latest version of the guidelines and focuses on making content more accessible to those with cognitive and learning disabilities, low vision, and mobile device users. It addresses Focus Appearance, Dragging Movements, Target Size, and Accessible Authentication.
Pa11y's features include a command-line interface, customizable configuration, defined actions, and reporting. It supports HTML CodeSniffer and Axe test runners, with Axe supporting WCAG 2.2 AA.
