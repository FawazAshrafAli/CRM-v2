async function populateGuest(guestType) {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: 'GET',
            url: '/activities/get_guests/',
            dataType: 'json',
            data: {
                'guest_type': guestType
            },
            success: function (data) {
                var name = guestType.toLowerCase();

                // $('#guest').prop('name', name);
                $('.guest').each(function () {
                    $(this).prop('name', name);
                });
                // $('#guest').html('<option disabled selected hidden>Select Guest</option>');
                $('.guest').each(function () {
                    $(this).html('<option disabled selected hidden>Select Guest</option>')
                });

                if ($('#edit-guest-input')) {
                $('#edit-guest-dropdown').prop('name', name);            
                $('#edit-guest-dropdown').html('<option disabled selected hidden>Select Guest</option>');
                }

                if ($('#guests')) {
                    $('#guests').prop('name', name + "s");
                    $('#guests').html('<option value="" disabled selected hidden>Select Guests</option>');
                };

                if ($('#edit-guests-dropdown')) {
                    $('#edit-guests-dropdown').prop('name', name + "s");
                    $('#edit-guests-dropdown').html('<option value="" disabled selected hidden>Select Guests</option>');
                };

                if (data.guest_data != null && Array.isArray(data.guest_data)) {
                    data.guest_data.forEach((guest) => {
                        html = `
                        <option value="" disabled selected hidden>Select ${guestType}</option>
                        <option value="${guest.id}">${guest.first_name} ${guest.last_name}</option>
                        `
                        // $('#guest').append(html);
                        $('.guest').each(function () {
                            $(this).append(html);
                        });

                        if ($('#edit-guest-dropdown')) {
                        $('#edit-guest-dropdown').append(html);
                        };

                        if ($('#guests')) {
                            $('#guests').append(html);
                        };

                        if ($('#edit-guests-dropdown')) {
                        $('#edit-guests-dropdown').append(html);
                        };
                    });
                };
                resolve();
            },
            error: function (error) {
                console.error("Error: ", error)
                reject(error);
            },
        });
    });
};