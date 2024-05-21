function updatePlan(planId) {
    $.ajax({
        type: 'GET',
        url: '/crm_admin/plan_details/' + planId,
        dataType: 'json',
        success: function (plan) {
            $('#plan-updation-form').prop('action', '/crm_admin/update_plan/' + planId);

            if (plan.name != null && plan.name != '') {
                $('#plan-name-value').val(plan.name);
            } else {
                $('#plan-name-value').val('');
            };

            if (plan.duration != null && plan.duration != '') {
                $('#duration-value').val(plan.duration);
            } else {
                $('#duration-value').val('');
            };


            $('#plan-updation-btn').prop('disabled', true);

            $('#plan-updation-form').on('input', function () {
                if ($('#plan-name-value').val() != plan.name || $('#duration-value').val() != plan.duration ) {
                    $('#plan-updation-btn').prop('disabled', false);
                } else {
                    $('#plan-updation-btn').prop('disabled', true);
                };
            });
            
        },
        error: function (error) {
            console.error('Error: ', error);
        },
    });
};
