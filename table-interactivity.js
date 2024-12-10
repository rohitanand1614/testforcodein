document.addEventListener("DOMContentLoaded", function () {
    // Add expand/collapse toggle for each table
    const tables = document.querySelectorAll(".expandable-table");
    tables.forEach((table) => {
        const toggle = document.createElement("button");
        toggle.textContent = "Expand/Collapse";
        toggle.style.marginBottom = "10px";
        toggle.onclick = () => {
            const rows = table.querySelectorAll("tr:not(:first-child)");
            rows.forEach((row) => {
                row.style.display =
                    row.style.display === "none" ? "table-row" : "none";
            });
        };
        table.parentNode.insertBefore(toggle, table);

        // Initially collapse all rows except the header
        const rows = table.querySelectorAll("tr:not(:first-child)");
        rows.forEach((row) => (row.style.display = "none"));
    });

    // Add sorting functionality
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
