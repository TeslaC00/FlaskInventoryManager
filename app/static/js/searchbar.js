// Function to filter the table rows based on the search input
function searchTables() {
    // Declare variables
    var input, filter, tables, table, tr, td, i, j, txtValue, rowText, searchWords, match;

    input = document.getElementById("searchInput");
    filter = input.value.toLowerCase().trim();  // convert input to lowercase and trim whitespace

    // If the search input is empty, show all rows and return
    if (filter === "") {
        tables = document.getElementsByClassName("searchableTable");
        for (let k = 0; k < tables.length; k++) {
            table = tables[k];
            tr = table.getElementsByTagName("tr");
            for (i = 0; i < tr.length; i++) {
                tr[i].style.display = "";  // show all rows
            }
        }
        return;
    }

    // Split the search input into individual words
    searchWords = filter.split(/\s+/);

    tables = document.getElementsByClassName("searchableTable");  // get all tables with the class "searchableTable"

    // Loop through all tables
    for (let k = 0; k < tables.length; k++) {
        table = tables[k];
        tr = table.getElementsByTagName("tr");

        // Loop through all table rows
        for (i = 0; i < tr.length; i++) {
            tr[i].style.display = "";  // show all rows by default
            td = tr[i].getElementsByTagName("td");
            rowText = "";

            // Concatenate text content of all cells in the row
            for (j = 0; j < td.length; j++) {
                if (td[j]) {
                    rowText += td[j].textContent.toLowerCase() + " ";
                }
            }
            rowText = rowText.trim();

            // Check if all search words match the rowText
            match = true;
            for (let word of searchWords) {
                // Find the index of the current search word in the row text
                const wordIndex = rowText.indexOf(word);
                if (wordIndex === -1 || wordIndex !== 0) { // If the word is not found or not at the beginning, set match to false
                    match = false;
                    break;
                }
                // Remove the matched word from the row text to prevent re-matching
                rowText = rowText.slice(wordIndex + word.length).trim();
            }

            // If not all search words matched, hide the row
            if (!match) {
                tr[i].style.display = "none";
            }
        }
    }
}

// Add event listener to the search input field to trigger the search function as the user types
document.getElementById("searchInput").addEventListener("input", searchTables);
