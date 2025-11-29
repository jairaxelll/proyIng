// HTML Text Indexer - JavaScript Functions

function selectAll() {
    const checkboxes = document.querySelectorAll('.activity-checkbox');
    checkboxes.forEach(cb => cb.checked = true);
}

function deselectAll() {
    const checkboxes = document.querySelectorAll('.activity-checkbox');
    checkboxes.forEach(cb => cb.checked = false);
}

function selectBasic() {
    const checkboxes = document.querySelectorAll('.activity-checkbox');
    checkboxes.forEach((cb, index) => {
        cb.checked = index < 4; // Activities 1-4
    });
}

function selectAdvanced() {
    const checkboxes = document.querySelectorAll('.activity-checkbox');
    checkboxes.forEach((cb, index) => {
        cb.checked = index >= 4; // Activities 5-11
    });
}

// Add event listeners when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const checkboxes = form.querySelectorAll('input[type="checkbox"][name="activity"]');
            if (checkboxes.length > 0) {
                const checked = Array.from(checkboxes).some(cb => cb.checked);
                if (!checked) {
                    e.preventDefault();
                    alert('Please select at least one activity to run.');
                    return false;
                }
            }
        });
    });
});


