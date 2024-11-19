// Hero Carousel
let currentIndex: number = 0;
const carousel: HTMLElement | null = document.getElementById("carousel");
const slides: number = carousel?.children.length || 0;
let startX: number;
let isDragging: boolean = false;

function showSlide(index: number): void {
    if (carousel) {
        carousel.style.transform = `translateX(-${index * 100}%)`;

        const dots: NodeListOf<Element> = document.querySelectorAll(".w-3");
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

function heroButtonVisibility(index: number): void {
    const hero_b_right = document.getElementById('hero-button-right') as HTMLElement
    const hero_b_left = document.getElementById('hero-button-left') as HTMLElement
    if (index === slides-1  && hero_b_right && hero_b_left) {
        hero_b_right.classList.add('opacity-0');
        hero_b_left.classList.remove('opacity-0');
    }else if (index === 0  && hero_b_left && hero_b_right) {
        hero_b_left.classList.add('opacity-0');
        hero_b_right.classList.remove('opacity-0');
    }else {
        if (hero_b_left && hero_b_right) {
            hero_b_left.classList.remove('opacity-0');
            hero_b_right.classList.remove('opacity-0');
        }
    }
}

function prevSlide(): void {
    currentIndex = currentIndex > 0 ? currentIndex - 1 : slides - 1;
    heroButtonVisibility(currentIndex);
    showSlide(currentIndex);
}

function nextSlide(): void {
    currentIndex = (currentIndex + 1) % slides;
    heroButtonVisibility(currentIndex);
    showSlide(currentIndex);
}

function goToSlide(index: number): void {
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
        if (!isDragging) return;

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
        } else if (walk > 50) {
            prevSlide();
        } else {
            showSlide(currentIndex);
        }
        carousel.classList.remove('cursor-grabbing');
    });
}

setInterval(() => {
    nextSlide();
}, 5000);

const firstDot: HTMLElement | null = document.getElementById("dot0");
if (firstDot) firstDot.classList.add("bg-indigo-500");


// Swipe Container
const swiperContainer = document.querySelectorAll('.swiper-container') as NodeListOf<HTMLElement>;;
swiperContainer.forEach((container) => {
    const images = container.getElementsByTagName('img');
    
    Array.from(images).forEach((img) => {
        img.draggable = false;
    });

    // Biar tombolnya bisa ilang
    const leftButton = document.getElementById('left-button') as HTMLElement;
    const rightButton = document.getElementById('right-button') as HTMLElement;
    function checkScrollPosition(): void {
        const maxScrollLeft = container.scrollWidth - container.clientWidth;
    
        if (container.scrollLeft <= 0) {
            leftButton.classList.add('opacity-0'); 
        } else {
            leftButton.classList.remove('opacity-0');
        }
    
        if (container.scrollLeft >= maxScrollLeft) {
            rightButton.classList.add('opacity-0'); 
        } else {
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
    let startX: number;
    let scrollLeft: number;

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
        if (!isDown) return;
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
    const overlay = document.getElementById('overlay') as HTMLElement;
    let hideTimeout: number | null = null;

    if (dropdownBackgroundEffect && overlay) {
        const showBackground = (): void => {
            if (hideTimeout) {
                clearTimeout(hideTimeout);
            }
            overlay.classList.remove('hidden');
        };

        const hideBackground = (): void => {
            hideTimeout = setTimeout(() => {
                overlay.classList.add('hidden');
            }, 200)
        };

        dropdownBackgroundEffect.forEach((items) => {
            items.addEventListener('mouseenter', showBackground);
            items.addEventListener('mouseleave', hideBackground);
        })

        overlay.addEventListener('click', hideBackground);
    }
});

// CART
const cartInteract =  document.querySelectorAll<HTMLElement>('.wishlist, .remove-from-cart');

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
const sortButton = document.getElementById('sortDropdown') as HTMLElement;
const icon = sortButton.querySelector('div span i') as HTMLElement;
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
        } else {
            icon.classList.remove('rotate-180');
        }
        flip = !flip;
    }
}

function sortButonText(pilihan: string) {
    const sortingText = sortButton.querySelector('h1');
    if (sortingText){
        sortingText.innerText = pilihan;
    }
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

let searchView = false;
function DisplayMode (){
    const DisplayButton = document.getElementById('DisplayButton')?.querySelector('i');
    const searchList = document.getElementById('searchList');
    const searchColumn = document.getElementById('searchColumn');

    if (searchList && searchColumn && DisplayButton) {
        DisplayButton.classList.toggle('fa-grip');
        DisplayButton.classList.toggle('fa-list');

        searchList.classList.toggle('hidden');

        searchColumn.classList.toggle('hidden');
        searchColumn.classList.toggle('grid');
    }
}

function rotateAccordionIcon(accordion: string) {
    const accordionIcon = document.getElementById(accordion)?.querySelector('button span i');

    if (accordionIcon) {
        accordionIcon.classList.toggle('rotate-180');
    }
}