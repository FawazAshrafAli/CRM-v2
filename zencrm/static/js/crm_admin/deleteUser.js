function deleteUser(userId) {
    $.ajax({
        type: 'GET',
        url: '/crm_admin/user_details/' + userId,
        dataType: 'json',
        success: function (user) {
            $('#user-deletion-form').prop('action', '/crm_admin/delete_user/' + userId)

            if (user.full_name != null && user.full_name != '') {
                $('#user-deletion-object').html(user.full_name);
            } else {
                $('#user-deletion-object').html('');
            };
        },
        error: function (error) {
            console.error('Error: ', error);
        }
    });
};