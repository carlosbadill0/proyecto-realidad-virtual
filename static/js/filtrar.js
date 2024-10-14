document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const table = document.getElementById('userTable');
    const noResultsMessage = document.getElementById('noResultsMessage');

    if (searchInput && table && noResultsMessage) {
        const rows = table.getElementsByTagName('tr');

        searchInput.addEventListener('input', function() {
            const filter = searchInput.value.toLowerCase();
            let hasResults = false;

            for (let i = 1; i < rows.length; i++) { // Start from 1 to skip table header
                let cells = rows[i].getElementsByTagName('td');
                let match = false;

                for (let j = 0; j < cells.length; j++) {
                    if (cells[j]) {
                        if (cells[j].innerText.toLowerCase().indexOf(filter) > -1) {
                            match = true;
                            break;
                        }
                    }
                }

                if (match) {
                    rows[i].style.display = '';
                    hasResults = true;
                } else {
                    rows[i].style.display = 'none';
                }
            }

            if (hasResults) {
                noResultsMessage.style.display = 'none';
            } else {
                noResultsMessage.style.display = 'block';
            }
        });
    }
});