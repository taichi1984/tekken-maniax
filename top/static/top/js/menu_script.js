document.addEventListener('DOMContentLoaded', function() {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const menu = document.querySelector('.site_menu');

    hamburgerMenu.addEventListener('click', function() {
        menu.classList.toggle('show');
    });
});