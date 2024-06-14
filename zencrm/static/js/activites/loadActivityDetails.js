function loadActivityDetails(activityId) {
  $.ajax({
      type: 'GET',
      url: '/activities/detail/' + activityId,
      dataType: 'json',
      success: data => {
        
        if (data) {
          if (data.activity) {
            $('.activity-type').html(data.activity);  
          } else {
            $('.activity-type').html('None');
          };

          if (data.id) {
            $('.activity-id').html(data.id);
          } else {
            $('.activity-id').html('None');
          };

          if (data.host) {
            $('.host').html(data.host);            
          } else {
            $('.host').html('None');
          };

          if (data.guest_type) {
            $('.guest-type').html(data.guest_type);
          } else {
            $('.guest-type').html('None');
          };
          
          $('.guest-title').html('Guest');
          if (data.guest) {
            $('.guest').html(data.guest);
          } else if (data.guests && Array.isArray(data.guests)) {
            $('.guest-title').html('Guests');
            let guest_data = '';              
            for (var i = 0; i < data.guests.length; i++) {
              if (i != data.guests.length - 1) {
                guest_data += `${data.guests[i]}, `;
              } else {
                guest_data += `${data.guests[i]}`;
              };
            };              
            $('.guest').html(guest_data);              
          } else {
            $('.guest').html('None');
          };

          if (data.phone) {
            $('.phone').html(data.phone);
          } else {
            $('.phone').html('None');
          };

          if (data.email) {
            $('.email').html(data.email);
          } else {
            $('.email').html('None');
          };

          if (data.owner) {
            $('.owner').html(data.owner);
          } else {
            $('.owner').html('None');
          };

          if (data.starting_datetime) {
            $('.starting-datetime').html(data.starting_datetime);
          } else {
            $('.starting-datetime').html('None');
          };

          if (data.ending_datetime) {
            $('.ending-datetime').html(data.ending_datetime);
          } else {
            $('.ending-datetime').html('None');
          };
          
          if (data.user_responsible) {
              $('.user-responsible').html(data.user_responsible);
            } else {
              $('.user-responsible').html('None');
            };

          if (data.activity == "Meeting" || data.activity == "Meal") {
            
            $('#title-div').show();
            $('#purpose-div').show();
            $('#location-div').show();

            if (data.title) {
              $('.title').html(data.title);
            } else {
              $('.title').html('None');
            };

            if (data.purpose) {
              $('.purpose').html(data.purpose);
            } else {
              $('.purpose').html('None');
            };              

            if (data.location) {
              $('.location').html(data.location);
            } else {
              $('.location').html('None');
            };

          } else {
            $('#title-div').hide();
            $('#purpose-div').hide();
            $('#location-div').hide();
          };

          if (data.activity == "Meal") {
            $('#additional-information-div').show();
            if (data.additional_information) {
              $('.additional-information').html(data.additional_information);
            } else {
              $('.additional-information').html('None');
            };
          } else {
            $('#additional-information-div').hide();
          };

          $('.notes').each(function () {
            if (data.notes) {
              $(this).html(data.notes);
            } else {
              $(this).html('None');
            };
          })

        };
      },
      error: error => console.error('Error', error),
  });
};