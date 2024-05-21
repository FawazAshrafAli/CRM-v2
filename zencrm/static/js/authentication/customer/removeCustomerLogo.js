function removeCustomerLogo(customerId){
    $.ajax({
        type: 'GET',
        url: '/authentication/remove_customer_logo/' + customerId,
        dataType: 'json',
        success: function (data) {
            $('.website-logo').each(function () {
                $(this).prop('src', '/static/images/zencrm_logo.png');
            });
            $('#website-logo').prop('style', '')

        },
        error: function (error) {
            console.error('Error: ', error);
        }
    });
};