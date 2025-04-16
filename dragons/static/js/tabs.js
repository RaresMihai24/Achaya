function showTab(tabName) {
    // Hide all tab contents
    var contents = document.querySelectorAll('.tab-content');
    contents.forEach(function(content) {
        content.style.display = 'none';
    });
    // Show the requested tab
    document.getElementById(tabName).style.display = 'block';
    // Remove "active" class from all tabs, then add to the clicked tab
    var tabs = document.querySelectorAll('.tab');
    tabs.forEach(function(tab) {
        tab.classList.remove('active');
    });
    // In this example, the event is passed in by the onclick attribute or can be looked up separately;
    // you may need to adjust how the active class is applied.
}
document.addEventListener('DOMContentLoaded', function() {
    showTab('characteristics'); // Set the default tab to display once the page is loaded.
});

function toggleRename() {
    const form = document.getElementById('renameForm');
    form.style.display = form.style.display === 'none' ? 'flex' : 'none';
    if (form.style.display === 'flex') {
        form.querySelector('input[name="new_name"]').focus();
    }
}

    function openRenameOverlay() {
        document.getElementById("renameOverlay").style.display = "flex";
    }
