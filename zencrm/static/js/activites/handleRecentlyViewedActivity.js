function handleRecentlyViewedActivity(activityId) {
    $.ajax({
        type: 'POST',
        url: '/activities/handle_recently_viewed/',
        datatype: 'json',
        data: {
            'activity_id': activityId
        },
        success: data => {
            if (data.message) {
                console.log(data.message);
            };
        },
        error: error => {
            console.error("Error", error);
        },
      });
    };