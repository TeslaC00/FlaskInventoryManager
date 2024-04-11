// Function to filter the table rows based on the search input
function searchTable() {
    // Declare variables
    var input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("materialTableBody");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those that don't match the search query
    for (i = 0; i < tr.length; i++) {
        tr[i].style.display = "none";  // hide all rows by default
        td = tr[i].getElementsByTagName("td");
        for (j = 0; j < td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = ""; // show the row if the search term is found in any column
                    break; // break out of the inner loop once a match is found
                }
            }
        }
    }
}

// Add event listener to the search input field to trigger the search function as the user types
document.getElementById("searchInput").addEventListener("input", searchTable);
