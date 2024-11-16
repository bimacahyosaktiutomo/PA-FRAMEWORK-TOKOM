"use strict";
let isMinimized = false;
function toggleSideBar() {
    const sidebar = document.getElementById('sidebar');
    const sidebar_off_canvas = document.getElementById('sidebar-off-canvas');
    const hamburger_button_container = document.getElementById('hamburger-button-container');
    const hidden_hamburger_button = document.getElementById('hidden-hamburger-button');
    const descendant = sidebar.querySelectorAll('i, span, #sidebar-name');
    const sidebar_item = sidebar.querySelectorAll('.sidebar-item');
    if (window.innerWidth >= 768) {
        if (!isMinimized) {
            sidebar.classList.remove('w-2/12');
            sidebar.classList.add('w-20');
            hamburger_button_container.classList.remove('w-2/12');
            hamburger_button_container.classList.add('w-20');
            if (window.innerWidth < 768) {
                sidebar.classList;
            }
            Array.from(descendant).forEach((e) => {
                if (!e.classList.contains('sidebar-icon')) {
                    e.classList.add('hidden');
                }
            });
            Array.from(sidebar_item).forEach((e) => {
                e.classList.remove('justify-between');
                e.classList.add('justify-center');
            });
        }
        else {
            sidebar.classList.remove('w-20');
            sidebar.classList.add('w-2/12');
            hamburger_button_container.classList.remove('w-20');
            hamburger_button_container.classList.add('w-2/12');
            Array.from(descendant).forEach((e) => {
                if (!e.classList.contains('sidebar-icon')) {
                    e.classList.remove('hidden');
                }
            });
            Array.from(sidebar_item).forEach((e) => {
                e.classList.remove('justify-center');
                e.classList.add('justify-between');
            });
        }
    }
    else {
        if (!isMinimized) {
            sidebar_off_canvas.classList.remove('-translate-x-full');
            sidebar_off_canvas.classList.add('translate-x-0');
            hidden_hamburger_button.classList.add('rotate-90');
            hidden_hamburger_button.classList.remove('fa-bars');
            hidden_hamburger_button.classList.add('fa-x');
        }
        else {
            sidebar_off_canvas.classList.add('-translate-x-full');
            sidebar_off_canvas.classList.remove('translate-x-0');
            hidden_hamburger_button.classList.remove('rotate-90');
            hidden_hamburger_button.classList.remove('fa-x');
            hidden_hamburger_button.classList.add('fa-bars');
        }
    }
    isMinimized = !isMinimized;
}
// Select all <li> elements in both sidebars
const sidebarItems = document.querySelectorAll('#sidebar li, #sidebar-off-canvas li');
sidebarItems.forEach((item) => {
    item.addEventListener('click', function (event) {
        event.preventDefault();
        // Remove 'active' class from all <li> elements
        // sidebarItems.forEach((i) => i.classList.remove('bg-indigo-700'));
        // Add 'active' class to the clicked <li> element
        // item.classList.add('bg-indigo-700');
        // Find the index of the clicked item and add 'active' to the corresponding item in the other sidebar
        const itemIndex = Array.from(sidebarItems).indexOf(item) % (sidebarItems.length / 2);
        const matchingItem = sidebarItems[itemIndex + sidebarItems.length / 2];
        // matchingItem.classList.add('bg-indigo-700');
    });
});
