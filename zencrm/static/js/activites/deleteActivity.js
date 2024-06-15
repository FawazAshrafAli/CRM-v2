function deleteActivity(activityId) {
    $.ajax({
        type: 'GET',
        url: '/activities/detail/' + activityId,
        dataType: 'json',
        success: data => {
            $('#delete-activity-form').prop('action', '/activities/delete/' + activityId);

            if (data.activity) {
                $('#deleting-activity-object').html(data.activity);
            } else {
                $('#deleting-activity-object').html('');
            };

        },
        error: error => {
            console.error("Error: ", error);
        },
    });
};