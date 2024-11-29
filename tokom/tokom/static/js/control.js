"use strict";
// Hero Carousel
let currentIndex = 0;
const carousel = document.getElementById("carousel");
const slides = (carousel === null || carousel === void 0 ? void 0 : carousel.children.length) || 0;
let startX;
let isDragging = false;
function showSlide(index) {
    if (carousel) {
        carousel.style.transform = `translateX(-${index * 100}%)`;
        const dots = document.querySelectorAll(".w-3");
        dots.forEach((dot, i) => {
            dot.classList.remove("bg-indigo-500");
            dot.classList.add("bg-gray-400");
            if (i === index) {
                dot.classList.remove("bg-gray-400");
                dot.classList.add("bg-indigo-500");
            }
        });
    }
}
function heroButtonVisibility(index) {
    const hero_b_right = document.getElementById('hero-button-right');
    const hero_b_left = document.getElementById('hero-button-left');
    if (index === slides - 1 && hero_b_right && hero_b_left) {
        hero_b_right.classList.add('opacity-0');
        hero_b_left.classList.remove('opacity-0');
    }
    else if (index === 0 && hero_b_left && hero_b_right) {
        hero_b_left.classList.add('opacity-0');
        hero_b_right.classList.remove('opacity-0');
    }
    else {
        if (hero_b_left && hero_b_right) {
            hero_b_left.classList.remove('opacity-0');
            hero_b_right.classList.remove('opacity-0');
        }
    }
}
function prevSlide() {
    currentIndex = currentIndex > 0 ? currentIndex - 1 : slides - 1;
    heroButtonVisibility(currentIndex);
    showSlide(currentIndex);
}
function nextSlide() {
    currentIndex = (currentIndex + 1) % slides;
    heroButtonVisibility(currentIndex);
    showSlide(currentIndex);
}
function goToSlide(index) {
    currentIndex = index;
    heroButtonVisibility(currentIndex);
    showSlide(currentIndex);
}
heroButtonVisibility(currentIndex);
if (carousel) {
    carousel.addEventListener('mousedown', (event) => {
        startX = event.pageX - carousel.offsetLeft;
        isDragging = true;
        carousel.classList.add('cursor-grab');
    });
    carousel.addEventListener('mouseup', () => {
        isDragging = false;
        carousel.classList.remove('cursor-grab');
    });
    carousel.addEventListener('mouseleave', () => {
        isDragging = false;
        carousel.classList.remove('cursor-grab');
    });
    carousel.addEventListener('mousemove', (event) => {
        if (!isDragging)
            return;
        const x = event.pageX - carousel.offsetLeft;
        const walk = (x - startX) * 3;
        carousel.style.transform = `translateX(-${currentIndex * 100 + walk / carousel.clientWidth * 100}%)`;
    });
    carousel.addEventListener('mouseup', (event) => {
        isDragging = false;
        const x = event.pageX - carousel.offsetLeft;
        const walk = (x - startX) * 3;
        if (walk < -50) {
            nextSlide();
        }
        else if (walk > 50) {
            prevSlide();
        }
        else {
            showSlide(currentIndex);
        }
        carousel.classList.remove('cursor-grabbing');
    });
}
setInterval(() => {
    nextSlide();
}, 5000);
const firstDot = document.getElementById("dot0");
if (firstDot)
    firstDot.classList.add("bg-indigo-500");
// Swipe Container
const swiperContainer = document.querySelectorAll('.swiper-container');
;
swiperContainer.forEach((container) => {
    const images = container.getElementsByTagName('img');
    Array.from(images).forEach((img) => {
        img.draggable = false;
    });
    // Biar tombolnya bisa ilang
    const leftButton = document.getElementById('left-button');
    const rightButton = document.getElementById('right-button');
    function checkScrollPosition() {
        const maxScrollLeft = container.scrollWidth - container.clientWidth;
        if (container.scrollLeft <= 0) {
            leftButton.classList.add('opacity-0');
        }
        else {
            leftButton.classList.remove('opacity-0');
        }
        if (container.scrollLeft >= maxScrollLeft) {
            rightButton.classList.add('opacity-0');
        }
        else {
            rightButton.classList.remove('opacity-0');
        }
    }
    rightButton.addEventListener('click', () => {
        container.scrollBy({ left: 200, behavior: 'smooth' });
    });
    leftButton.addEventListener('click', () => {
        container.scrollBy({ left: -200, behavior: 'smooth' });
    });
    container.addEventListener('scroll', checkScrollPosition);
    checkScrollPosition();
    // Biar bisa di geser pake mouse
    let isDown = false;
    let startX;
    let scrollLeft;
    container.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - container.offsetLeft;
        scrollLeft = container.scrollLeft;
        container.classList.add('cursor-default');
    });
    container.addEventListener('mouseleave', () => {
        isDown = false;
        container.classList.add('cursor-default');
    });
    container.addEventListener('mouseup', () => {
        isDown = false;
        container.classList.add('cursor-default');
    });
    container.addEventListener('mousemove', (e) => {
        if (!isDown)
            return;
        e.preventDefault();
        const x = e.pageX - container.offsetLeft;
        const walk = (x - startX) * 0.8; // perkaliannya nentuin kecepatan gesernya
        container.scrollLeft = scrollLeft - walk;
    });
});
// BUat pas baru ngeload halaman
document.addEventListener('DOMContentLoaded', () => {
    // Darken Background
    const dropdownBackgroundEffect = document.querySelectorAll('#cartDropdownHover , #UserDropdown');
    const overlay = document.getElementById('overlay');
    let hideTimeout = null;
    if (dropdownBackgroundEffect && overlay) {
        const showBackground = () => {
            if (hideTimeout) {
                clearTimeout(hideTimeout);
            }
            overlay.classList.remove('hidden');
        };
        const hideBackground = () => {
            hideTimeout = setTimeout(() => {
                overlay.classList.add('hidden');
            }, 200);
        };
        dropdownBackgroundEffect.forEach((items) => {
            items.addEventListener('mouseenter', showBackground);
            items.addEventListener('mouseleave', hideBackground);
        });
        overlay.addEventListener('click', hideBackground);
    }
    // Review
    reviewStar('1');
});
// CART
const cartInteract = document.querySelectorAll('.wishlist, .remove-from-cart');
cartInteract.forEach((item) => {
    item.addEventListener('mouseenter', () => {
        item.classList.remove('fa-regular');
        item.classList.add('fa-solid');
    });
    item.addEventListener('mouseleave', () => {
        item.classList.remove('fa-solid');
        item.classList.add('fa-regular');
    });
});
// Search
const sortButton = document.getElementById('sortDropdown');
const icon = sortButton.querySelector('div span i');
let flip = true;
function sortButonFocusOut() {
    if (icon) {
        if (!flip) {
            icon.classList.remove('rotate-180');
            flip = !flip;
        }
    }
}
function sortButonIcon() {
    if (icon) {
        if (flip) {
            icon.classList.add('rotate-180');
        }
        else {
            icon.classList.remove('rotate-180');
        }
        flip = !flip;
    }
}
// function sortButonText(sortOption = null) {
//     // Change the button text to reflect the selected sort option
//     var sortText = document.getElementById('sortDropdownText')
//     if (sortText) {
//         sortText.textContent = sortOption
//     }
//     // Call the updateFilters function to update the URL with the selected sort option
//     updateFilters(sortOption);
// }
function updateFilters(sortOption = null, viewOption) {
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);
    const checkboxes = document.querySelectorAll('#accordion-kategori input[type="checkbox"]');
    // Clear existing category filters
    params.delete('c');
    // Append checked categories to the query parameters
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            params.append('c', checkbox.value);
        }
    });
    // Add or update the sort parameter
    if (sortOption) {
        params.set('sort', sortOption);
    }
    let viewOptionText;
    if (viewOption) {
        if (viewOption === true) {
            viewOptionText = 'grid';
            params.set('view', viewOptionText);
        }
        else {
            viewOptionText = 'list';
            params.set('view', viewOptionText);
        }
    }
    // Update the URL and reload the page
    window.location.href = `${url.pathname}?${params.toString()}`;
}
// let searchView = false;
// function searchViewMode (){
//     const searchViewButton = document.getElementById('searchViewButton')?.querySelector('i')
//     const searchList = document.getElementById('searchList');
//     const searchColumn = document.getElementById('searchColumn');
//     if (searchList && searchColumn && searchViewButton) {
//         if (searchView) {
//             searchViewButton.classList.remove('fa-grip');
//             searchViewButton.classList.add('fa-list');
//             searchList.classList.remove('hidden');
//             searchColumn.classList.add('hidden');
//             searchColumn.classList.remove('grid');
//         } else {
//             searchViewButton.classList.remove('fa-list');
//             searchViewButton.classList.add('fa-grip');
//             searchList.classList.add('hidden');
//             searchColumn.classList.remove('hidden');
//             searchColumn.classList.add('grid');
//         }
//         searchView = !searchView;
//     }
// }
function rotateAccordionIcon(accordion) {
    var _a;
    const accordionIcon = (_a = document.getElementById(accordion)) === null || _a === void 0 ? void 0 : _a.querySelector('button span i');
    if (accordionIcon) {
        accordionIcon.classList.toggle('rotate-180');
    }
}
// let searchView = true;
function DisplayMode() {
    var _a;
    const DisplayButton = (_a = document.getElementById('DisplayButton')) === null || _a === void 0 ? void 0 : _a.querySelector('i');
    const searchList = document.getElementById('searchList');
    const searchColumn = document.getElementById('searchColumn');
    if (searchList && searchColumn && DisplayButton) {
        DisplayButton.classList.toggle('fa-grip');
        DisplayButton.classList.toggle('fa-list');
        searchList.classList.toggle('hidden');
        searchColumn.classList.toggle('hidden');
        searchColumn.classList.toggle('grid');
        // searchView = !searchView
        // updateFilters(null, searchView)
    }
}
function sortOrderHistory() {
    var _a, _b;
    const historyContainer = document.getElementById('orderHistoryContainer');
    const orderHistorySortButton = document.getElementById('orderHistorySortButton');
    const sortTextElement = orderHistorySortButton.querySelector('p');
    if (historyContainer && orderHistorySortButton) {
        historyContainer.classList.toggle('flex-col');
        historyContainer.classList.toggle('flex-col-reverse');
        (_a = orderHistorySortButton.querySelector('i')) === null || _a === void 0 ? void 0 : _a.classList.toggle('rotate-180');
        if (sortTextElement) {
            const currentText = (_b = sortTextElement.textContent) === null || _b === void 0 ? void 0 : _b.trim(); // Trim the text to remove extra spaces
            sortTextElement.textContent = currentText === "Newest" ? "Oldest" : "Newest";
        }
    }
}
// Review
var isRated = false;
var lastRatingValue = '1';
function reviewStar(ratingValue) {
    let inputValue = document.getElementById('ratingReviewValue');
    const starContainer = document.getElementById('starContainer');
    if (lastRatingValue === ratingValue) {
        inputValue.value = '1';
        lastRatingValue = '1';
    }
    else {
        inputValue.value = ratingValue;
        lastRatingValue = ratingValue;
    }
    if (starContainer) {
        Array.from(starContainer.children).forEach((e, index) => {
            const child = e;
            if (child.nodeType === Node.ELEMENT_NODE && index < parseInt(inputValue.value)) {
                child.classList.remove('fa-reguler');
                child.classList.add('fa-solid');
                child.classList.add('text-yellow-300');
            }
            else if (child.nodeType === Node.ELEMENT_NODE) {
                child.classList.add('fa-reguler');
                child.classList.remove('fa-solid');
                child.classList.remove('text-yellow-300');
            }
        });
        console.log(inputValue.value);
    }
}
