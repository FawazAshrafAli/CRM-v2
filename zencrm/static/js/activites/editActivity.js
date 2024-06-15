async function editActivity(activityId) {
  $.ajax({
      type: 'GET',
      url: '/activities/detail/' + activityId,
      dataType: 'json',
      success: async(data) => {
        
        if (data) {
          $('#activity-updation-form').prop('action', `/activities/update/${activityId}`);

          if (data.activity) {
            $(`#edit-toggle-${data.activity.toLowerCase()}-btn`).click();
            $('#edit-activity-input').val(data.activity);
          } else {
            $('#edit-activity-input').val('');
          };

          if (data.guest_type) {
            await populateGuest(data.guest_type);
          };            

          // Fetching Selected Guest Type
          const editGuestTypeDropdown = document.getElementById('edit-guest-type-dropdown');           

          for (let i = 0; i < editGuestTypeDropdown.options.length; i++) {
            if (data.guest_type) {
              if (editGuestTypeDropdown.options[i].value == data.guest_type) {
                  editGuestTypeDropdown.options[i].selected = true;
              } else {
                  editGuestTypeDropdown.options[i].selected = false;
              };
            } else {
                editGuestTypeDropdown.options[i].selected = false;                
            };
          };
          
          // Fetching Selected Guest
          const editGuestDropdown = document.getElementById('edit-guest-dropdown');

          for (let i = 0; i < editGuestDropdown.options.length; i++) {
            if (data.guest_id) {
              if (editGuestDropdown.options[i].value == data.guest_id) {
                  editGuestDropdown.options[i].selected = true;
              } else {
                  editGuestDropdown.options[i].selected = false;
              };
            } else {
                editGuestDropdown.options[0].selected = true;                
            };
          };

          // Fetching Selected Guest(S)
          const editGuestsDropdown = document.getElementById('edit-guests-dropdown');

          for (let i = 0; i < editGuestsDropdown.options.length; i++) {
            if (data.guests_id && Array.isArray(data.guests_id)) {
              for (let j = 0; j < data.guests_id.length; j++) {
                if (editGuestsDropdown.options[i].value == data.guests_id[j]) {
                    editGuestsDropdown.options[i].selected = true;
                };
              };
            } else {
              editGuestsDropdown.options[i].selected = false;
              };
            };

          if (data.guests) {
            $('#edit-add-guests').click();
          } else {
            $('.dismiss-guest-btn').click();
          };

          if (data.purpose) {
            $('#edit-add-description').click();
          } else {
            $('.dismiss-description-btn').click();
          };
          
          if (data.location) {
            $('#edit-add-location').click();
          } else {
            $('.dismiss-location-btn').click();
          }
          
          if (data.host) {
            $('#edit-host-input').val(data.host);            
          } else {
            $('#edit-host-input').val('');
          };

          if (data.title) {
            $('#edit-title-input').val(data.title);            
          } else {
            $('#edit-title-input').val('');
          };

          if (data.purpose) {
            $('#edit-purpose-input').val(data.purpose);            
          } else {
            $('#edit-purpose-input').val('');
          };

          if (data.starting_date) {
            $('#edit-starting-date-input').val(data.starting_date);
          } else {
            $('#edit-starting-date-input').val('');
          };

          if (data.starting_time) {
            $('#edit-starting-time-input').val(data.starting_time);
          } else {
            $('#edit-starting-time-input').val('');
          };

          if (data.ending_date) {
            $('#edit-ending-date-input').val(data.ending_date);
          } else {
            $('#edit-ending-date-input').val('');
          };

          if (data.ending_time) {
            $('#edit-ending-time-input').val(data.ending_time);
          } else {
            $('#edit-ending-time-input').val('');
          };
          
          const editUserResponsibleDropdown = document.getElementById('edit-user-responsible-dropdown');
          
          for (let i = 0; i < editUserResponsibleDropdown.options.length; i++) {            
            if (data.user_responsible_id) {
              if (editUserResponsibleDropdown.options[i].value == data.user_responsible_id) {
                  editUserResponsibleDropdown.options[i].selected = true;
              } else {
                  editUserResponsibleDropdown.options[i].selected = false;
              };
            } else {
              editUserResponsibleDropdown.options[i].selected = false;
            };              
          };

          if (data.notes) {
            $('#edit-notes-input').val(data.notes);
          } else {
            $('#edit-notes-input').val('');
          };

          if (data.location) {
            $('#edit-location-input').val(data.location);
          } else {
            $('#edit-location-input').val('');
          };

          if (data.additional_information) {
            $('#edit-additional-info').val(data.additional_information);
          } else {
            $('#edit-additional-info').val('');
          };

          if (data.closed && data.closed == true) {
            $('#edit-closed-input').prop('checked', true);
          } else {
            $('#edit-closed-input').prop('checked', false);
          };

        };
      },
      error: error => console.error('Error', error),
  });
};