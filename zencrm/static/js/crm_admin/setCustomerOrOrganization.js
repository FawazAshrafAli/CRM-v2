function setOrganization(customerName) {
    var customerSelectValue = customerName.value
    var organizationSelect = document.getElementById('organization-select');

    for (var i = 0; i < organizationSelect.options.length; i++) {
        if (organizationSelect.options[i].value == customerSelectValue) {
            organizationSelect.options[i].selected = true;
        } else {
            organizationSelect.options[i].selected = false;
        };
    };				
};

function setCustomer(organizationName) {
    var organizationSelectValue = organizationName.value
    var customerSelect = document.getElementById('customer-select');

    for (var i = 0; i < customerSelect.options.length; i++) {
        if (customerSelect.options[i].value == organizationSelectValue) {
            customerSelect.options[i].selected = true;
        } else {
            customerSelect.options[i].selected = false;
        };
    };				
};