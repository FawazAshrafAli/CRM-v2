function loadActivityDetails(activityId) {
    $.ajax({
        type: 'GET',
        url: '/activities/detail/' + activityId,
        dataType: 'json',
        success: data => {
            $('#host-guest').html('');

            data.activity_data.map((activity) => {
                html = `<tr>
                <td class="border-0">Record ID</td>
                <td class="border-0">${activity.id}</td>
              </tr>
              <tr>
                <td class="border-0">Host</td>
                <td class="border-0">${activity.host}</td>
              </tr>
              <tr>
                <td>Guest</td>
                <td>${activity.guest}</td>
              </tr>`    
            });
        },
        error: error => console.error('Error', error),
    });
};