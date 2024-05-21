function deletePlan(planId) {
    $.ajax({
        type: 'GET',
        url: '/crm_admin/plan_details/' + planId,
        dataType: 'json',
        success: function (plan) {
            $('#plan-deletion-form').prop('action', '/crm_admin/delete_plan/' + planId);

            if (plan.name != null && plan.name != '') {
                $('#plan-deletion-object').html(plan.name);
            } else {
                $('#plan-deletion-object').html('');
            };
            
        },
        error: function (error) {
            console.error('Error: ', error);
        },
    });
};
