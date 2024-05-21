function activateCustomer (customerId) {
    $.ajax({
        type: 'Get',
        url: '/crm_admin/customer_detail/' + customerId,
        dataType: 'json',
        success: function (customer) {
            $('#customer-activation-form').prop('action', '/crm_admin/activate_customer/' + customerId);

            if (customer.name != null && customer.name != '') {
                $('#activating-customer-object').html(customer.name);
            } else {
                $('#activating-customer-object').html('');
            };
        },
        error: function (error) {
            console.error('Error: ', error);
        }
    })
}