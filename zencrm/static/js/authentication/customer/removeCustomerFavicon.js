function removeCustomerFavicon(customerId){    
    $.ajax({
        type: 'GET',
        url: '/authentication/remove_customer_favicon/' + customerId,
        dataType: 'json',
        success: function (data) {            
            $('#website-favicon').prop('href', '/static/images/zencrm_mini_logo.png');            
        },
        error: function (error) {
            console.error('Error: ', error);
        }
    });
};