function deactivateCustomer (customerId) {
    $.ajax({
        type: 'GET',
        url: '/crm_admin/customer_detail/' + customerId,
        dataType: 'json',
        success: function (customer) {
            $('#deactivate-customer-form').prop('action', '/crm_admin/deactivate_customer/' + customerId);

            if (customer.name != null && customer.name != '') {
                $('#deactivating-customer-object').html(customer.name);
            } else {
                $('#deactivating-customer-object').html('');
            };
        },
        error: function (error) {
            console.error();
        },
    });
};