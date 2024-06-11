// const addAdvanceOptions = document.getElementById('add-advance-options');
//   const guest = document.getElementById('guest');
//   const additionalInformation = document.getElementById('additional-information');
//   const advanceOptions = document.getElementById('advanced-options');
//   const meetingTitle = document.getElementById('meeting-title');

//   var currentActivity = document.getElementById('activity');
  
//   function toggleDefault() {
//     meetingTitle.style.display = 'none';
//     additionalInformation.style.display = 'none';

//     defaultAdvancedOptions();
//   }

//   function toggleCall() {
//     currentActivity.value = 'Call';

//     toggleDefault();
//     addAdvanceOptions.style.display = 'none';
//     guest.style.display = 'block';

//   };

//   function toggleMeeting() {      
//     currentActivity.value = 'Meeting';

//     toggleDefault();

//     advanceOptions.style.display = 'block';
//     meetingTitle.style.display = 'block';
//   };

//   // function toggleReminder() {      
//   //   currentActivity.value = 'Reminder';
//   // };

//   // function toggleFlagged() {      
//   //   currentActivity.value = 'Flagged';
//   // };

//   // function toggleEmail() {      
//   //   currentActivity.value = 'Email';
//   // };

//   function toggleMeal() {      
//     currentActivity.value = 'Meal';

//     advanceOptions.style.display = 'block';
//     additionalInformation.style.display = 'block';
//   };
  
//   document.getElementById('toggle-call-btn').addEventListener('click', toggleCall);

//   document.getElementById('toggle-meeting-btn').addEventListener('click', toggleMeeting);
//   // document.getElementById('toggle-reminder-btn').addEventListener('click', toggleReminder);
//   // document.getElementById('toggle-flagged-btn').addEventListener('click', toggleFlagged);
//   // document.getElementById('toggle-email-btn').addEventListener('click', toggleEmail);
//   document.getElementById('toggle-meal-btn').addEventListener('click', toggleMeal);
//   document.getElementById('edit-toggle-meal-btn').addEventListener('click', toggleMeal);





//   // Decleration
//   const addGuests = document.getElementById('add-guests');
//   const addLocation = document.getElementById('add-location');
//   const addDescription = document.getElementById('add-desciption');
  
//   const guestInputDiv = document.getElementById('guest-input-div');
//   const locationInputDiv = document.getElementById('location-input-div');
//   const descriptionInputDiv = document.getElementById('description-input-div');

//   // Default Behavior of Advance Options
//   function defaultAdvancedOptions() {
//     addAdvanceOptions.style.display = 'block';

//     addGuests.style.display = 'inline';
//     addLocation.style.display = 'inline';
//     addDescription.style.display = 'inline';

//     guestInputDiv.style.display = 'none';
//     locationInputDiv.style.display = 'none';
//     descriptionInputDiv.style.display = 'none';
//   };

//   // Hide Advance Options
//   function hideAdvanceOptions() {
//     const links = document.querySelectorAll('#add-advance-options span');

//     let hiddenCount = 0;

//     links.forEach(link => {
//       if (getComputedStyle(link).display === 'none') {
//         hiddenCount++;
//       };
//       if (hiddenCount == links.length) {
//         addAdvanceOptions.style.display = 'none';
//       } else {
//         addAdvanceOptions.style.display = 'block';
//       }
//     });
//   };

//   // Set Div Visibility
//   function setDivVisibility(hidingDivId, showingDivId) {
//     hidingDivId.style.display = 'none';
//     showingDivId.style.display = 'inline';
//     hideAdvanceOptions();
//   }


//   // Toggle Guests
//   addGuests.addEventListener('click', function() {
//     setDivVisibility(addGuests, guestInputDiv);
//     guest.style.display = 'none';

//     for (var i = 0; i < guest.options.length; i++) {
//       if (i == 0) {
//         guest.options[i].selected = true;
//       } else {
//         guest.options[i].selected = false;
//       };
//     };
//   });

//   // Toggle Location
//   addLocation.addEventListener('click', function () {
//     setDivVisibility(addLocation, locationInputDiv);
//   });

//   // Toggle Description
//   addDescription.addEventListener('click', function () {
//     setDivVisibility(addDescription, descriptionInputDiv);
//   });

//   // Close Guests Input
//   document.getElementById('dismiss-guests-btn').addEventListener('click', () => {
//     setDivVisibility(guestInputDiv, addGuests);
//     guest.style.display = 'block';

//     const guests = document.getElementById('guests');
//     for (var i = 0; i < guests.options.length; i++) {
//       guests.options[i].selected = false;
//     };

//   });

//   // Close Location Input
//   document.getElementById('dismiss-location-btn').addEventListener('click', () => {
//     setDivVisibility(locationInputDiv, addLocation);
//   });

//   // Close Description Input
//   document.getElementById('dismiss-description-btn').addEventListener('click', () => {
//     setDivVisibility(descriptionInputDiv, addDescription);
//   });