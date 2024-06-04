function populateGuest(guestType) {
    $.ajax({
        type: 'GET',
        url: '/activities/get_guests/',
        dataType: 'json',
        data: {
            'guest_type': guestType
        },
        success: function (data) {
            var name = guestType.toLowerCase();

            $('#guest').prop('name', name);            
            $('#guest').html('<option disabled selected hidden>Select Guest</option>');

            if ($('#guests')) {
                $('#guests').prop('name', name + "s");
                $('#guests').html('<option disabled selected hidden>Select Guests</option>');
            };

            if (data.guest_data != null && Array.isArray(data.guest_data)) {
                data.guest_data.forEach((guest) => {
                    console.log(guest.id)
                    html = `
                    <option disabled selected hidden>Select ${guestType}</option>
                    <option value="${guest.id}">${guest.first_name} ${guest.last_name}</option>
                    `
                    $('#guest').append(html);

                    if ($('#guests')) {
                        $('#guests').append(html);
                    };
                });
            };
        },
        error: function (error) {
            console.log("Error: ", error)
        },
    });
};