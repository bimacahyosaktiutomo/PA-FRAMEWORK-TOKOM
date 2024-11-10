class CustomButtonComponent {
    eGui;
    eButtonEdit;
    eButtonDelete;
    eventListenerEdit;
    eventListenerDelete;

    init(params) {
        this.eGui = document.createElement('div');
        this.eGui.className = 'flex justify-evenly';

        // Edit button setup
        this.eButtonEdit = document.createElement('button');
        this.eButtonEdit.className = 'px-2 rounded-md bg-blue-500 text-blue-50 hover:bg-blue-600 hover:text-zinc-900 hover-anim';
        const iconEdit = document.createElement('i');
        iconEdit.className = 'fa-regular fa-pen-to-square';
        this.eButtonEdit.appendChild(iconEdit);

        // Delete button setup
        this.eButtonDelete = document.createElement('button');
        this.eButtonDelete.className = 'px-2 rounded-md bg-red-500 text-red-50 hover:bg-red-600 hover:text-zinc-900 hover-anim';
        const iconDelete = document.createElement('i');
        iconDelete.className = 'fa-solid fa-trash';
        this.eButtonDelete.appendChild(iconDelete);

        // Event listeners
        this.eventListenerEdit = () => alert('Edit button clicked');
        this.eventListenerDelete = () => alert('Delete button clicked');
        this.eButtonEdit.addEventListener('click', this.eventListenerEdit);
        this.eButtonDelete.addEventListener('click', this.eventListenerDelete);

        // Append buttons to the GUI element
        this.eGui.appendChild(this.eButtonEdit);
        this.eGui.appendChild(this.eButtonDelete);
    }

    getGui() {
        return this.eGui;
    }

    refresh(params) {
        return true;
    }

    destroy() {
        if (this.eButtonEdit) {
            this.eButtonEdit.removeEventListener("click", this.eventListenerEdit);
        }
        if (this.eButtonDelete) {
            this.eButtonDelete.removeEventListener("click", this.eventListenerDelete);
        }
    }
}

function getColumnDefs() {
    if (window.innerWidth >= 540) {
        return [
            { field: "nama", flex: 2 },
            { field: "deskripsi", flex: 2 },
            { field: "kategori", flex: 1 },
            { field: "rating", flex: 1 },
            { field: "stok", flex: 1 },
            { field: "diskon", flex: 1 },
            { field: "harga", filter: "agNumberColumnFilter", flex: 1 },
            { field: "aksi", cellRenderer: CustomButtonComponent, filter: false, flex: 1 },
        ];
    } else {
        return [
            { field: "nama", flex: 2 },
            { field: "kategori", flex: 1 },
            { field: "aksi", cellRenderer: CustomButtonComponent, filter: false, flex: 1 },
        ];
    }
}

function getPagination () {
    if (window.innerWidth >= 540) {
        return true
    } else {
        return false;
    }
}

var gridOptions = {
    rowData: [
        { nama: "AMD Ryzen 5 5600X", deskripsi: "6-Core 12-Thread Unlocked Desktop Processor", kategori: "Processor", rating: 4.7, stok: 120, diskon: 10, harga: 199, gambar: "https://example.com/ryzen5-5600x.jpg" },
        { nama: "NVIDIA GeForce RTX 3070", deskripsi: "8GB GDDR6 PCI Express 4.0 Graphics Card", kategori: "Graphics Card", rating: 4.9, stok: 80, diskon: 15, harga: 499, gambar: "https://example.com/rtx3070.jpg" },
        { nama: "Corsair Vengeance LPX 16GB", deskripsi: "DDR4 DRAM 3200MHz C16 Desktop Memory Kit", kategori: "Memory", rating: 4.6, stok: 200, diskon: 5, harga: 74, gambar: "https://example.com/vengeancelpx.jpg" },
        { nama: "Samsung 970 EVO Plus 1TB", deskripsi: "M.2 NVMe Internal SSD", kategori: "Storage", rating: 4.8, stok: 150, diskon: 12, harga: 149, gambar: "https://example.com/970evoplus.jpg" },
        { nama: "ASUS ROG Strix B550-F Gaming", deskripsi: "AMD AM4 TUF Gaming Motherboard", kategori: "Motherboard", rating: 4.5, stok: 90, diskon: 8, harga: 189, gambar: "https://example.com/strixb550.jpg" },
    ],
    columnDefs: getColumnDefs(),
    defaultColDef: {
        filter: "agTextColumnFilter",
        floatingFilter: true,
    },
    pagination: getPagination(),
    paginationPageSize: 10,
};


// -------------- PENTING --------------- //
const myGridElement = document.querySelector("#barangGrid");
const api = agGrid.createGrid(myGridElement, gridOptions);
// -------------- PENTING --------------- //

function destroyGrid() { // Ngehapus grid, referensi saja
    api.destroy();
}

window.addEventListener("resize", () => {

    // Buat ngubah header kolom sesuai ukuran
    if (window.innerWidth <= 540) {
        const newColumnDefs = getColumnDefs();
        api.setGridOption("columnDefs", newColumnDefs);

        const newPagination = getPagination();
        api.setGridOption("pagination", newPagination );
    } else {
        const newColumnDefs = getColumnDefs();
        api.setGridOption("columnDefs", newColumnDefs);
        
        const newPagination = getPagination();
        api.setGridOption("pagination", newPagination );
    }
});