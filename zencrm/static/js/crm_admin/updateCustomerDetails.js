function updateCustomerDetails(customerId) {
    $.ajax({
        type: 'GET',
        url: '/crm_admin/customer_detail/' + customerId,
        dataType: 'json',
        success: function (customer) {
            $('#edit-customer-form').prop('action', '/crm_admin/update_customer/' + customerId);

            if (customer.name != null && customer.name != '') {
                $('#customer-name-value').val(customer.name);
            } else {
                $('#customer-name-value').val('');
            };

            if (customer.website_name != null && customer.website_name != '') {
                $('#website-name-value').val(customer.website_name);
            } else {
                $('#website-name-value').val('');
            };

            if (customer.organization != null && customer.organization != '') {
                $('#organization-name-value').val(customer.organization);
            } else {
                $('#organization-name-value').val('');
            };

            var typeOfOrganizationValue = document.getElementById('type-of-organization-value');
            
            for(var i = 0; i < typeOfOrganizationValue.options.length; i++) {
                if (customer.type_of_organization != null && customer.type_of_organization != '') {
                    if (typeOfOrganizationValue.options[i].value == customer.type_of_organization) {
                        typeOfOrganizationValue.options[i].selected = true;
                    } else {
                        typeOfOrganizationValue.options[i].selected = false;
                    };
                } else {
                    typeOfOrganizationValue.options[i].selected = false;
                };
            };

            if (customer.logo != null) {
                $('#logo-value').html(customer.logo).prop('href', customer.logo);
            } else {
                $('#logo-value').html('').prop('href', '#');
            };

            if (customer.favicon != null) {
                $('#favicon-value').html(customer.favicon).prop('href', customer.favicon);
            } else {
                $('#favicon-value').html('').prop('href', '#');
            };

            if (customer.email != null && customer.email != '') {
                $('#email-value').val(customer.email);
            } else {
                $('#email-value').val('');
            };

            if (customer.phone != null && customer.phone != '') {
                $('#phone-value').val(customer.phone);
            } else {
                $('#phone-value').val('');
            };

            var planValue = document.getElementById('plan-value');
            
            for(var i = 0; i < planValue.options.length; i++) {
                if (customer.plan != null && customer.plan != '') {
                    if (planValue.options[i].value == customer.plan) {
                        planValue.options[i].selected = true;
                    } else {
                        planValue.options[i].selected = false;
                    };
                } else {
                    planValue.options[i].selected = false;
                };
            };

            if (customer.no_of_users != null && customer.no_of_users != '') {
                $('#no-of-users-value').val(customer.no_of_users);
            } else {
                $('#no-of-users-value').val('');
            };

        },
        error: function (error) {
            console.error("Error: ", error);
        }
    })
}