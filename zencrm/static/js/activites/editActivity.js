function editActivity(activityId) {
    $.ajax({
        type: 'GET',
        url: '/activities/detail/' + activityId,
        dataType: 'json',
        success: data => {
          
          if (data) {
            if (data.activity) {
              $('#edit-activity-input').val(data.activity);
            } else {
              $('#edit-activity-input').val('');
            };
  
            // if (data.id) {
            //   $('.activity-id').html(data.id);
            // } else {
            //   $('.activity-id').html('None');
            // };
  
            if (data.host) {
              $('#edit-host-input').val(data.host);            
            } else {
              $('#edit-host-input').val('');
            };
  
            const editGuestType = $('#edit-guest-dropdown');
            
            for (var i = 0; i < editGuestType.options.length; i++) {
                if (data.guest_type) {
                    if (editGuestType.options[i].value === data.guest_type) {
                        editGuestType.options[i].selected = true;
                    } else {
                        editGuestType.options[i].selected = false;
                    };
                } else {
                    editGuestType.options[i].selected = false;
                };
            };

            
            
            
            const editGuestDropdown = $('#edit-guest-dropdown');
            
            for (var i = 0; i < editGuestDropdown.options.lenght; i++) {

                if (data.guest) {
                    if (editGuestDropdown.options[i].value === data.guest) {
                        editGuestDropdown.options[i].selected = true;
                    } else {
                        editGuestDropdown.options[i].selected = false;
                    };
                } else {
                    editGuestDropdown.options[i].selected = false;                
                };
            };


            const editGuestsDropdown = $('#edit-guests-dropdown');

            for (var i = 0; i < editGuestsDropdown.options.lenght; i++) {
                if (data.guests && Array.isArray(data.guests)) {
                    for (var guest in data.guests) {
                        if (editGuestsDropdown.options[i].value === guest) {
                            editGuestsDropdown.options[i].selected = true;
                        } else {
                            editGuestsDropdown.options[i].selected = false;
                        };
                    };
                } else {
                    editGuestsDropdown.options[i].selected = false;
                };
            };

  
            if (data.phone) {
              $('#edit-phone-input').val(data.phone);
            } else {
              $('#edit-phone-input').val('');
            };
  
            if (data.email) {
              $('#edit-email-input').val(data.email);
            } else {
              $('#edit-email-input').val('');
            };
  
            if (data.owner) {
              $('#edit-owner-input').val(data.owner);
            } else {
              $('#edit-owner-input').val('');
            };
  
            if (data.starting_datetime) {
              $('#edit-starting-datetime-input').val(data.starting_datetime);
            } else {
              $('#edit-starting-datetime-input').val('');
            };
  
            if (data.ending_datetime) {
              $('#edit-ending-datetime-input').html(data.ending_datetime);
            } else {
              $('#edit-ending-datetime-input').html('');
            };
            
            if (data.user_responsible) {

                var editUserResponsibleDropdown = $('#edit-user-responsible-dropdown');

                for (var i = 0; i < editUserResponsibleDropdown.options.length; i++) {
                    if (editUserResponsibleDropdown.options[i].value === data.user_responsible) {
                        editUserResponsibleDropdown.options[i].selected = true;
                    } else {
                        editUserResponsibleDropdown.options[i].selected = false;
                    };
                };
                
            };
              
          };
        },
        error: error => console.error('Error', error),
    });
  };