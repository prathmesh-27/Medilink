document.getElementById("Search").addEventListener("keyup", function () {
    var input = this.value.toLowerCase();
    var rows = document.querySelectorAll("#searchable_table tbody tr");

    rows.forEach(function (row) {
        var name = row.cells[0].textContent.toLowerCase();
        row.style.display = name.includes(input) ? "" : "none";
    });
});