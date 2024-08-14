document.getElementById('mobile-menu').addEventListener('click', function() {
    const navLinks = document.getElementById('nav-links');
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
});

function changeMainImage(event) {
    const mainImage = event.target.closest('.car-detail-container').querySelector('.main-image');
    mainImage.src = event.target.src;
}

document.querySelector('form').addEventListener('submit', function(event) {
    const checkedBoxes = document.querySelectorAll('input[name="delete_image_ids"]:checked');
    if (checkedBoxes.length > 0) {
        const confirmDeletion = confirm('Are you sure you want to delete the selected images?');
        if (!confirmDeletion) {
            event.preventDefault(); // Prevent form submission if the user cancels
        }
    }
});

// script.js

// Sidebar toggle function
function toggleSidebar() {
    document.body.classList.toggle('sidebar-open');
    
    // Save the sidebar state in local storage
    if (document.body.classList.contains('sidebar-open')) {
        localStorage.setItem('sidebarState', 'open');
    } else {
        localStorage.setItem('sidebarState', 'closed');
    }
}

// Add click event to the toggle button
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior
            toggleSidebar();
        });
    }

    // Check the sidebar state on page load
    if (localStorage.getItem('sidebarState') === 'open') {
        document.body.classList.add('sidebar-open');
    }
});

// Mobile menu toggle (if applicable)
document.getElementById('mobile-menu').onclick = function() {
    document.getElementById('nav-links').classList.toggle('nav-open');
};
