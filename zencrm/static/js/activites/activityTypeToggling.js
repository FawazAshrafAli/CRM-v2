// Default Behavior of Advance Options
function defaultAdvancedOptions() {

    $('.add-advance-options').each(function () {
      $(this).show();
    });

    $('.add-guests').each(function () {
      $(this).show()
    });

    $('.add-location').each(function () {
      $(this).show();
    });

    $('.add-desciption').each(function () {
      $(this).show();
    });

    $('.guest-input-div').each(function () {
      $(this).hide();
    });

    $('.location-input-div').each(function () {
      $(this).hide();
    });

    $('.description-input-div').each(function () {
      $(this).hide();
    });

  };

  function toggleDefault() {
    $('.title-div').each(function () {
      $(this).hide();
    });

    $('.additional-info-div').each(function () {
      $(this).hide();
    });

    defaultAdvancedOptions();
  }

  function toggleCall() {
    $('.activity').each(function () {
      $(this).val('Call');
    });

    toggleDefault();
    $('.advanced-options').each(function () {
      $(this).hide();
    });

    $('.guest-div').each(function () {
      $(this).show();
    });
  };

  function toggleMeeting() {    
    $('.activity').each(function () {
      $(this).val('Meeting');
    });

    toggleDefault();

    $('.advanced-options').each(function () {
      $(this).show();
    });

    $('.title-div').each(function () {
      $(this).show();
    });
  };

  // function toggleReminder() {      
  //   currentActivity.value = 'Reminder';
  // };

  // function toggleFlagged() {      
  //   currentActivity.value = 'Flagged';
  // };

  // function toggleEmail() {      
  //   currentActivity.value = 'Email';
  // };

  function toggleMeal() {      
    $('.activity').each(function () {
      $(this).val('Meal');
    });

    toggleDefault();

    $('.advanced-options').each(function () {
      $(this).show();
    });

    $('.title-div').each(function () {
      $(this).show();
    });

    $('.additional-info-div').each(function () {
      $(this).show();
    });
  };
  
  $('.toggle-call-btn').on('click', toggleCall);
  $('.toggle-meeting-btn').on('click', toggleMeeting);

  // document.getElementById('toggle-reminder-btn').addEventListener('click', toggleReminder);
  // document.getElementById('toggle-flagged-btn').addEventListener('click', toggleFlagged);
  // document.getElementById('toggle-email-btn').addEventListener('click', toggleEmail);
  $('.toggle-meal-btn').on('click', toggleMeal);

  // Hide Advance Options
  function hideAdvanceOptions() {
    const links = document.querySelectorAll('.add-advance-options span');

    let hiddenCount = 0;

    links.forEach(link => {
      if (getComputedStyle(link).display === 'none') {
        hiddenCount++;
      };
      if (hiddenCount == links.length) {
        $('.add-advance-options').each(function () {
          $(this).hide();
        });
      } else {
        $('.add-advance-options').each(function () {
          $(this).show();
        });
      }
    });
  };

  // Set Div Visibility
  function setDivVisibility(hidingDivId, showingDivId) {
    hidingDivId.each(function () {
      $(this).hide();
    });

    showingDivId.each(function () {
      $(this).show();
    });
    hideAdvanceOptions();
  }


  // Toggle Guests
  $('.add-guests').on('click', function() {
    setDivVisibility($('.add-guests'), $('.guest-input-div'));

    $('.guest-div').each(function () {
      $(this).hide()
    });

    $('.guest-dropdown').each(function() {
      var $dropdown = $(this);
      $dropdown.find('option').each(function(index) {
        if (index === 0) {
          $(this).prop('selected', true);
        } else {
          $(this).prop('selected', false);
        }
      });
    });
  });

  // Toggle Location
  $('.add-location').on('click', function () {
    setDivVisibility($('.add-location'), $('.location-input-div'));
  });

  // Toggle Description
  $('.add-desciption').on('click', function () {
    setDivVisibility($('.add-desciption'), $('.description-input-div'));
  });

  // Close Guests Input
  $('.dismiss-guests-btn').on('click', () => {
    setDivVisibility($('.guest-input-div'), $('.add-guests'));

    $('.guest-div').each(function () {
      $(this).show()
    });

    const guests = document.getElementById('guests');
    for (var i = 0; i < guests.options.length; i++) {
      guests.options[i].selected = false;
    };

  });

  // Close Location Input
  $('.dismiss-location-btn').on('click', () => {
    setDivVisibility($('.location-input-div'), $('.add-location'));
  });

  // Close Description Input
  $('.dismiss-description-btn').on('click', () => {
    setDivVisibility($('.description-input-div'), $('.add-desciption'));
  });