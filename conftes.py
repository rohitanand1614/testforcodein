import pytest
from py.xml import html


def pytest_html_report_title(report):
    report.title = "Accessibility Test Report"


def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Violations"))


def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.violations or "No violations"))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if call.when == "call":
        violations = getattr(item, "violations", None)
        if violations:
            report.violations = html_table(violations)
        else:
            report.violations = "No violations"


@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([
        html.script(src="table-interactivity.js"),
        html.link(rel="stylesheet", href="table-style.css"),
    ])


def html_table(violations):
    """Construct an interactive HTML table for violations."""
    table = html.table(
        cls="expandable-table sortable",
        border="1",
        style="border-collapse: collapse; width: 100%;"
    )
    # Add table headers
    table.append(
        html.tr(
            [
                html.th("Violation Type"),
                html.th("Impact"),
                html.th("Help"),
                html.th("Selectors"),
            ]
        )
    )
    # Add rows for each violation
    for v in violations:
        table.append(
            html.tr(
                [
                    html.td(v["type"]),
                    html.td(v.get("impact", "N/A")),
                    html.td(v["help"]),
                    html.td(", ".join(v["selector"])),
                ]
            )
        )
    return table
