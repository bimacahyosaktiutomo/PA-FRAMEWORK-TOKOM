let isMinimized = false;
function toggleSideBar(): void {
  const sidebar = document.getElementById("sidebar") as HTMLElement;
  const overlay = document.getElementById('overlay') as HTMLElement;
  // const sidebar_off_canvas = document.getElementById(
  //   "sidebar-off-canvas"
  // ) as HTMLElement;
  const hamburger_button_container = document.getElementById(
    "hamburger-button-container"
  ) as HTMLElement;
  const hidden_hamburger_button = document.getElementById(
    "hidden-hamburger-button"
  ) as HTMLElement;
  const descendant = sidebar.querySelectorAll("i, span, #sidebar-name");
  const sidebar_item = sidebar.querySelectorAll(".sidebar-item");

  if (window.innerWidth >= 768) {
    if (!isMinimized) {
      sidebar.classList.remove("w-2/12");
      sidebar.classList.add("w-20");
      hamburger_button_container.classList.remove("w-2/12");
      hamburger_button_container.classList.add("w-20");
      if (window.innerWidth < 768) {
        sidebar.classList;
      }
      Array.from(descendant).forEach((e) => {
        if (!e.classList.contains("sidebar-icon")) {
          e.classList.add("hidden");
        }
      });

      Array.from(sidebar_item).forEach((e) => {
        e.classList.remove("justify-between");
        e.classList.add("justify-center");
      });
    } else {
      sidebar.classList.remove("w-20");
      sidebar.classList.add("w-2/12");
      hamburger_button_container.classList.remove("w-20");
      hamburger_button_container.classList.add("w-2/12");
      Array.from(descendant).forEach((e) => {
        if (!e.classList.contains("sidebar-icon")) {
          e.classList.remove("hidden");
        }
      });

      Array.from(sidebar_item).forEach((e) => {
        e.classList.remove("justify-center");
        e.classList.add("justify-between");
      });
    }
  } else {
    if (!isMinimized) {
      sidebar.classList.remove("-translate-x-full");
      sidebar.classList.add("translate-x-0");
      hidden_hamburger_button.classList.add("rotate-90");
      hidden_hamburger_button.classList.remove("fa-bars");
      hidden_hamburger_button.classList.add("fa-x");
      overlay.classList.remove("hidden")
    } else {
      sidebar.classList.add("-translate-x-full");
      sidebar.classList.remove("translate-x-0");
      hidden_hamburger_button.classList.remove("rotate-90");
      hidden_hamburger_button.classList.remove("fa-x");
      hidden_hamburger_button.classList.add("fa-bars");
      overlay.classList.add("hidden")
    }
  }

  isMinimized = !isMinimized;
}

function toggleNewCategoryInput(): void {
    const categorySelect = document.getElementById("id_category") as HTMLSelectElement;
    const newCategoryInput = document.getElementById("id_new_category") as HTMLInputElement;

    if (categorySelect.value && categorySelect.selectedIndex > 1 ) {
        newCategoryInput.disabled = true; 
        newCategoryInput.value = ""; 
        categorySelect.disabled = false; 
    } else {
        
        newCategoryInput.disabled = false;
        if (!newCategoryInput.value) {
            categorySelect.disabled = false; 
        }
    }
}

window.onload = () => toggleNewCategoryInput();
const newCategoryInput = document.getElementById("id_new_category") as HTMLInputElement;
newCategoryInput.addEventListener('input', () => {
    const resetButton = document.getElementById("resetCategoryBtn") as HTMLButtonElement;
    const categorySelect = document.getElementById("id_category") as HTMLSelectElement;
    if (newCategoryInput.value) {
        categorySelect.selectedIndex = 1; 
        resetButton.disabled = true;
        categorySelect.disabled = true;
    } else {
        categorySelect.disabled = false;
        resetButton.disabled = false;
    }   
});

function resetCategorySelection(): void {
    const categorySelect = document.getElementById("id_category") as HTMLSelectElement;
    categorySelect.selectedIndex = 0;  
    toggleNewCategoryInput();
}

const resetButton = document.getElementById("resetCategoryBtn");
if (resetButton) {
    resetButton.addEventListener('click', resetCategorySelection);
}

function submitItemsHover (condition: number): void {
    const categorySelect = document.getElementById("id_category") as HTMLSelectElement;
    if (condition === 0){
        if (categorySelect.selectedIndex === 1 && categorySelect.disabled === true) {
            categorySelect.disabled = false;
        }
    } else if (condition === 1){
        if (categorySelect.selectedIndex === 1) {
            categorySelect.disabled = true;
        }
    }
}

function PreviewImage(): void{
  const fileInput = document.getElementById('id_image') as HTMLInputElement;

  if (fileInput.files) {
      const oFReader = new FileReader();
      oFReader.readAsDataURL(fileInput.files[0]);

      oFReader.onload = function (oFREvent) {
          const imgPreview = document.getElementById('imgPreview') as HTMLImageElement | null;
          if (imgPreview && oFREvent.target) {
              imgPreview.src = oFREvent.target.result as string;
          }
          imgPreview?.className
      };
  };
}