let currentSupplierId;

function populateEditModal(supplierId) {
    $.ajax({
        type: 'GET',
        url: `/api/supplier/${supplierId}`,
        success: function (supplier) {
            $('#editSupplierId').val(supplier.supplier_id);
            $('#editSupplierName').val(supplier.supplier_name);
            $('#editSupplierGSTNo').val(supplier.GST_No);
            $('#editSupplierStateCode').val(supplier.state_code);
            $('#editSupplierStateName').val(supplier.state_name);
            // Populate other fields
            $('#editSupplierModal').modal('show');
        }
    });
}

function submitEdit() {
    let supplierId = $('#editSupplierId').val();
    let formData = {
        name: $('#editSupplierName').val(),
        GST_No: $('#editSupplierGSTNo').val(),
        state_code: $('#editSupplierStateCode').val(),
        state_name: $('#editSupplierStateName').val(),
        csrf_token: $('#editSupplierForm input[name="csrf_token"]').val()
        // Collect other form data
    };
    $.ajax({
        type: 'POST',
        url: `/api/supplier/${supplierId}`,
        data: formData,
        success: function (response) {
            $('#editSupplierModal').modal('hide');
            location.reload(); // Optionally, only update the row in question
        }
    });
}

function showDeleteModal(supplierId) {
    currentSupplierId = supplierId;
    $('#deleteSupplierModal').modal('show');
}

function confirmDelete() {
    if (currentSupplierId) {
        $.ajax({
            type: 'POST',
            url: `/api/supplier/${currentSupplierId}/delete`,
            success: function () {
                $('#deleteSupplierModal').modal('hide');
                location.reload(); // Optionally, only remove the row from the table
            }
        });
    }
}
