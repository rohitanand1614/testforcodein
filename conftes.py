import pytest
from py.xml import html


def pytest_html_report_title(report):
    report.title = "Accessibility Test Report"


def pytest_html_results_table_header(cells):
    # Add a single column for Violations
    cells.insert(2, html.th("Violations"))


def pytest_html_results_table_row(report, cells):
    # Insert violations data into the row
    cells.insert(2, html.td(report.violations or "No violations"))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if call.when == "call":
        # Attach violations data
        violations = getattr(item, "violations", None)
        if violations:
            report.violations = html_table(violations)
        else:
            report.violations = "No violations"


@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix, summary, postfix):
    # Add the JavaScript and CSS for interactivity
    prefix.extend([
        html.style("""
            .expandable-table {
                border: 1px solid #ccc;
                border-collapse: collapse;
                width: 100%;
            }
            .expandable-table th,
            .expandable-table td {
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }
            .expandable-table th {
                background-color: #f2f2f2;
                cursor: pointer;
            }
            .expandable-table tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .expandable-table tr:hover {
                background-color: #f1f1f1;
            }
        """),
        html.script("""
            document.addEventListener("DOMContentLoaded", function () {
                const tables = document.querySelectorAll(".expandable-table");
                tables.forEach((table) => {
                    const toggle = document.createElement("button");
                    toggle.textContent = "Expand/Collapse";
                    toggle.style.marginBottom = "10px";
                    toggle.onclick = () => {
                        const rows = table.querySelectorAll("tr:not(:first-child)");
                        rows.forEach((row) => {
                            row.style.display = row.style.display === "none" ? "table-row" : "none";
                        });
                    };
                    table.parentNode.insertBefore(toggle, table);

                    // Initially collapse all rows except the header
                    const rows = table.querySelectorAll("tr:not(:first-child)");
                    rows.forEach((row) => (row.style.display = "none"));
                });

                const sortTable = (table, columnIndex, ascending) => {
                    const rows = Array.from(table.rows).slice(1);
                    rows.sort((a, b) => {
                        const aText = a.cells[columnIndex].textContent.trim();
                        const bText = b.cells[columnIndex].textContent.trim();
                        return ascending
                            ? aText.localeCompare(bText)
                            : bText.localeCompare(aText);
                    });
                    rows.forEach((row) => table.appendChild(row));
                };

                const headers = document.querySelectorAll(".sortable th");
                headers.forEach((header, index) => {
                    header.style.cursor = "pointer";
                    let ascending = true;
                    header.onclick = () => {
                        const table = header.closest("table");
                        sortTable(table, index, ascending);
                        ascending = !ascending;
                    };
                });
            });
        """)
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
