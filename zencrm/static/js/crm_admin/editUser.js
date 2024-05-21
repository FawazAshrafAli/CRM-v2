function editUser(userId) {
    $.ajax({
        type: 'GET',
        url: '/crm_admin/user_details/' + userId,
        dataType: 'json',
        success: function (user) {
            if (user.username != null && user.username != '') {
                $('#username-value').val(user.username);
            } else {
                $('#username-value').val('');
            };

            if (user.image != null && user.image != '') {
                $('#image-value').html(user.image).prop('href', user.image);
            } else {
                $('#image-value').html('').prop('href', '#');
            };

            if (user.first_name != null && user.first_name != '') {
                $('#first-name-value').val(user.first_name);
            } else {
                $('#first-name-value').val('');
            };

            if (user.last_name != null && user.last_name != '') {
                $('#last-name-value').val(user.last_name);
            } else {
                $('#last-name-value').val('');
            };

            if (user.email != null && user.email != '') {
                $('#email-value').val(user.email);
            } else {
                $('#email-value').val('');
            };

            if (user.phone != null && user.phone != '') {
                $('#phone-value').val(user.phone);
            } else {
                $('#phone-value').val('');
            };

            if (user.address != null && user.address != '') {
                $('#address-value').val(user.address);
            } else {
                $('#address-value').val('');
            };

            if (user.address_city != null && user.address_city != '') {
                $('#city-value').val(user.address_city);
            } else {
                $('#city-value').val('');
            };

            if (user.address_state != null && user.address_state != '') {
                $('#state-value').val(user.address_state);
            } else {
                $('#state-value').val('');
            };

            if (user.address_postal_code != null && user.address_postal_code != '') {
                $('#postal-code-value').val(user.address_postal_code);
            } else {
                $('#postal-code-value').val('');
            };

            var countrySelect = document.getElementById('country-select');

            for (var i = 0; i < countrySelect.options.length; i++) {
                if (user.address_country != null && user.address_country != '') {                    
                    if (countrySelect.options[i].value == user.address_country) {
                        countrySelect.options[i].selected = true;
                    } else {
                        countrySelect.options[i].selected = false;
                    };
                } else {
                    companySelect.options[i].selected = false;
                }
            };

            if (user.title != null && user.title != '') {
                $('#title-value').val(user.title);
            } else {
                $('#title-value').val('');
            };

            var genderSelect = document.getElementById('gender-select')

            for (var i = 0; i < genderSelect.options.length; i++) {
                if (user.gender != null && user.gender != '') {
                    if (genderSelect.options[i].value == user.gender) {
                        genderSelect.options[i].selected = true;
                    } else {
                        genderSelect.options[i].selected = false;
                    };
                } else {
                    genderSelect.options[i].selected = false;
                };
            };

            if (user.birthday != null && user.birthday != '') {
                $('#birthday-value').val(user.birthday);
            } else {
                $('#birthday-value').val('');
            };

            var companySelect = document.getElementById('company-select');

            for (var i = 0; i < companySelect.options.length; i++) {
                if (user.organization_id != null && user.organization_id != '') {
                    if (companySelect.options[i].value == user.organization_id) {                    
                        companySelect.options[i].selected = true;
                    } else {
                        companySelect.options[i].selected = false;
                    };
                } else {
                    companySelect.options[i].selected = false;
                };
            };

            if (user.team != null && user.team != '') {
                $('#team-value').val(user.team);
            } else {
                $('#team-value').val('');
            };

            var reportsToSelect = document.getElementById('reports-to-select');

            for (var i = 0; i < reportsToSelect.options.length; i++) {
                

                if (user.reports_to_id != null && user.reports_to_id != '') {
                    if (reportsToSelect.options[i].value == user.reports_to_id) {
                        reportsToSelect.options[i].selected = true;
                    } else {
                        reportsToSelect.options[i].selected = false;
                    };
                } else {
                    reportsToSelect.options[i].selected = false;
                };
            };

        },
        error: function(error) {
            console.error("Error: ", error);
        }
    });
};