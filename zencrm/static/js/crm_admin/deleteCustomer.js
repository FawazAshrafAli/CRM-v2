function deleteCustomer(customerId) {
    $.ajax({
        type: 'GET',
        url: '/crm_admin/customer_detail/' + customerId,
        dataType: 'json',
        success: function (customer) {
            $('#customer-deletion-form').prop('action', '/crm_admin/delete_customer/' + customerId);

            if (customer.name != 'null' && customer.name != '' && customer.organization != null && customer.organization != '') {
                $('#customer-deletion-object').html(customer.name + ' (' + customer.organization + ')');
                $('#deleting-organization-object').html(customer.organization);
            } else {
                $('#customer-deletion-object').html('');
                $('#deleting-organization-object').html('');
            };
            
        }, 
        error: function (error) {
            console.error('Error: ', error);
        }
    });
};