function loadCustomerDetails(customerId) {
    $.ajax({
        type: 'GET',
        url: '/crm_admin/customer_detail/' + customerId,
        dataType: 'json',
        success: function (customer) {
            if (customer.favicon != null) {
                $('#company-image').prop('src', customer.favicon)
            } else {
                $('#company-image').prop('src', '/static/assets/img/system-user.png')
            }
            
            $('.customer-name').each(function () {
                if (customer.name != null && customer.name != "") {                    
                    $(this).html(customer.name);
                } else {                    
                    $(this).html('');
                }
            });

            $('.customer-organization-id').each(function () {
                if (customer.organization_id != null && customer.organization_id != "") {                    
                    $(this).html(customer.organization_id);
                } else {                    
                    $(this).html('');
                }
            });

            $('.customer-organization').each(function () {
                if (customer.organization != null && customer.organization != "") {                    
                    $(this).html(customer.organization);
                } else {                    
                    $(this).html('');
                }
            });

            $('.customer-phone').each(function () {
                if (customer.phone != null && customer.phone != "") {                    
                    $(this).html(customer.phone);
                } else {                    
                    $(this).html('');
                }
            });

            $('.customer-email').each(function () {
                if (customer.email != null && customer.email != "") {                    
                    $(this).html(customer.email);
                } else {                    
                    $(this).html('');
                }
            });

            $('.customer-website-name').each(function () {
                if (customer.website_name != null && customer.website_name != "") {                    
                    $(this).html(customer.website_name);
                } else {                    
                    $(this).html('');
                }
            });

            $('.customer-no-of-users').each(function () {
                if (customer.no_of_users != null && customer.no_of_users != "") {                    
                    $(this).html(customer.no_of_users);
                } else {                    
                    $(this).html('');
                }
            });

            $('.customer-plan').each(function () {
                if (customer.plan != null && customer.plan != "") {                    
                    $(this).html(customer.plan);
                } else {                    
                    $(this).html('');
                }
            });

            $('.customer-amount').each(function () {
                if (customer.amount != null && customer.amount != "") {                    
                    $(this).html(customer.amount);
                } else {                    
                    $(this).html('');
                }
            });

            $('.customer-created-on').each(function () {
                if (customer.created != null && customer.created != "") {                    
                    $(this).html(customer.created);
                } else {                    
                    $(this).html('');
                }
            });

            $('.customer-expiry-date').each(function () {
                if (customer.expiry_date != null && customer.expiry_date != "") {
                    $(this).html(customer.expiry_date);
                } else {                    
                    $(this).html('');
                }
            });

        },
        error: function (error) {
            console.error("Error: ", error);
        }
    })
}