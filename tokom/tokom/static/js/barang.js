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
        this.eventListenerEdit = () => {
            const itemId = params.data.item_id;
            window.location.href = `edit_item/${itemId}`;
        };

        this.eventListenerDelete = () => {
            const itemId = params.data.item_id; // Get itemId from the row data
            const itemName = params.data.name
            confirmDelete(itemId, itemName); // Trigger confirmDelete with itemId
        };

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
            // this.eButtonEdit.removeEventListener("click", this.eventListenerEdit);
        }
        if (this.eButtonDelete) {
            // this.eButtonDelete.removeEventListener("click", this.eventListenerDelete);
        }
    }
}

function getColumnDefs() {
    if (window.innerWidth >= 540) {
        return [
            { field: "item_id", headerName: "Item ID", flex: 1 },
            { field: "name", headerName: "Name", flex: 2 },
            { field: "description", headerName: "Description", flex: 2 },
            { 
                field: "category", 
                headerName: "Category", 
                flex: 1, 
                valueFormatter: (params) => params.value?.name || 'No Category'
            },
            { field: "rating", headerName: "Rating", flex: 1 },
            { field: "stock", headerName: "Stock", flex: 1 },
            { field: "discount", headerName: "Discount", flex: 1 },
            { field: "price", headerName: "Price", filter: "agNumberColumnFilter", flex: 1 },
            { 
                field: "image", 
                headerName: "Image", 
                flex: 1,
                cellRenderer: (params) => {
                    return params.value ? `<img src="${params.value}" alt="Product Image" class="" />` : 'No Image';
                }
            },
            { field: "actions", headerName: "Actions", cellRenderer: CustomButtonComponent, filter: false, flex: 1 },
        ];
    } else {
        return [
            { field: "item_id", headerName: "Item ID", flex: 1 },
            { field: "name", headerName: "Name", flex: 2 },
            { field: "category", headerName: "Category", flex: 1, valueFormatter: (params) => params.value?.name || 'No Category'},
            { field: "actions", headerName: "Actions", cellRenderer: CustomButtonComponent, filter: false, flex: 1 },
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
    columnDefs: getColumnDefs(),
    defaultColDef: {
        filter: "agTextColumnFilter",
        floatingFilter: true,
    },
    rowModelType: 'infinite',
    cacheBlockSize: 20, // Number of rows to fetch per request
    datasource: {
        getRows: function(params) {
            const url = '/api/items/';  // Your API endpoint
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    params.successCallback(data, data.length);  // Pass data and total count
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    params.failCallback();
                });
        }
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

function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

function confirmDelete(itemsId, itemName) {
    Swal.fire({
        title: `Item akan dihapus ${itemName} ID : ${itemsId}`,
        text: `Item tidak akan bisa dikembalikan! ${itemName} ID : ${itemsId}`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ya, Hapus!'
    }).then((result) => {
        if (result.isConfirmed) {
            const csrfToken = getCSRFToken();
            // Ini AJAX
            fetch(`delete_item/${itemsId}/`, {
                method: 'POST',
                headers: {
                    // 'X-CSRFToken': '{{ csrf_token }}'
                    'X-CSRFToken': csrfToken 
                }
            }).then(response => {
                if (response.ok) {
                    Swal.fire(
                        'Deleted!',
                        'Item berhasil dihapus.',
                        'success'
                    ).then(() => {
                        // Reload the page after success
                        window.location.reload();
                    });
                } else {
                    Swal.fire(
                        'Error!',
                        'Gagal menghapus item.',
                        'error'
                    );
                }
            });
        }
    });
}