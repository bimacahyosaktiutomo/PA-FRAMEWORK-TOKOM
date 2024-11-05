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
