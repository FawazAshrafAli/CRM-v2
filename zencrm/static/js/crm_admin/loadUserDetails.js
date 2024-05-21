function loadUserDetails(userId) {
    $.ajax({
        type: 'GET',
        url: '/crm_admin/user_details/' + userId,
        dataType: 'json',
        success: function (user) {
            $('.user-id').each(function () {
                if (user.id != null && user.id != '') {
                    $(this).html(user.id);
                } else {
                    $(this).html('None');
                };
            });

            $('.user-image').each(function () {
                if (user.image != null && user.image != '') {
                    $(this).prop('src', user.image);
                } else {
                    $(this).prop('src', '/static/assets/img/system-user.png');
                };
            });

            $('.username').each(function () {
                if (user.username != null && user.username != '') {
                    $(this).html(user.username);
                } else {
                    $(this).html('None');
                };
            });

            $('.first-name').each(function () {
                if (user.first_name != null && user.first_name != '') {
                    $(this).html(user.first_name);
                } else {
                    $(this).html('None');
                };
            });

            $('.last-name').each(function () {
                if (user.last_name != null && user.last_name != '') {
                    $(this).html(user.last_name);
                } else {
                    $(this).html('None');
                };
            });

            $('.full-name').each(function () {
                if (user.full_name != null && user.full_name != '') {
                    $(this).html(user.full_name);
                } else {
                    $(this).html('None');
                };
            });

            $('.organization-id').each(function () {
                if (user.organization_id != null && user.organization_id != '') {
                    $(this).html(user.organization_id);
                } else {
                    $(this).html('None');
                };
            });

            $('.organization').each(function () {
                if (user.organization != null && user.organization != '') {
                    $(this).html(user.organization);
                } else {
                    $(this).html('None');
                };
            });

            $('.phone').each(function () {
                if (user.phone != null && user.phone != '') {
                    $(this).html(user.phone);
                } else {
                    $(this).html('None');
                };
            });

            $('.email').each(function () {
                if (user.email != null && user.email != '') {
                    $(this).html(user.email);
                } else {
                    $(this).html('None');
                };
            });

            $('.full-address').each(function () {
                if (user.full_address != null && user.full_address != '') {
                    $(this).html(user.full_address);
                } else {
                    $(this).html('None');
                };
            });

            $('.user-title').each(function () {
                if (user.title != null && user.title != '') {
                    $(this).html(user.title);
                } else {
                    $(this).html('None');
                };
            });

            $('.gender').each(function () {
                if (user.gender != null && user.gender != '') {
                    $(this).html(user.gender);
                } else {
                    $(this).html('None');
                };
            });

            $('.team').each(function () {
                if (user.team != null && user.team != '') {
                    $(this).html(user.team);
                } else {
                    $(this).html('None');
                };
            });

            $('.reports-to').each(function () {
                if (user.reports_to != null && user.reports_to != '') {
                    $(this).html(user.reports_to);
                } else {
                    $(this).html('None');
                };
            });

            $('.birthday').each(function () {
                if (user.birthday != null && user.birthday != '') {
                    $(this).html(user.birthday);
                } else {
                    $(this).html('None');
                };
            });

            $('.last-logged-in').each(function () {
                if (user.last_login != null && user.last_login != '') {
                    $(this).html(user.last_login);
                } else {
                    $(this).html('None');
                };
            });

            $('.created-on').each(function () {
                if (user.created != null && user.created != '') {
                    $(this).html(user.created);
                } else {
                    $(this).html('None');
                };
            });

            $('.updated-on').each(function () {
                if (user.updated != null && user.updated != '') {
                    $(this).html(user.updated);
                } else {
                    $(this).html('None');
                };
            });

            $('.passport-number').each(function () {
                if (user.passport_number != null && user.passport_number != '') {
                    $(this).html(user.passport_number);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.passport-expiry-date').each(function () {
                if (user.passport_expiry_date != null && user.passport_expiry_date != '') {
                    $(this).html(user.passport_expiry_date);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.telephone').each(function () {
                if (user.tel != null && user.tel != '') {
                    $(this).html(user.tel);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.nationality').each(function () {
                if (user.nationality != null && user.nationality != '') {
                    $(this).html(user.nationality);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.religion').each(function () {
                if (user.religion != null && user.religion != '') {
                    $(this).html(user.religion);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.maritial-status').each(function () {
                if (user.maritial_status != null && user.maritial_status != '') {
                    $(this).html(user.maritial_status);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.employment-of-spouse').each(function () {
                if (user.employment_of_spouse != null && user.employment_of_spouse != '') {
                    $(this).html(user.employment_of_spouse);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.number-of-children').each(function () {
                if (user.number_of_children != null && user.number_of_children != '') {
                    $(this).html(user.number_of_children);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.primary-contact-name').each(function () {
                if (user.primary_contact_name != null && user.primary_contact_name != '') {
                    $(this).html(user.primary_contact_name);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.primary-contact-relationship').each(function () {
                if (user.primary_contact_relationship != null && user.primary_contact_relationship != '') {
                    $(this).html(user.primary_contact_relationship);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.primary-contact-phone1').each(function () {
                if (user.primary_contact_phone1 != null && user.primary_contact_phone1 != '') {
                    $(this).html(user.primary_contact_phone1);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.primary-contact-phone2').each(function () {
                if (user.primary_contact_phone2 != null && user.primary_contact_phone2 != '') {
                    $(this).html(user.primary_contact_phone2);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.secondary-contact-name').each(function () {
                if (user.secondary_contact_name != null && user.secondary_contact_name != '') {
                    $(this).html(user.secondary_contact_name);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.secondary-contact-relationship').each(function () {
                if (user.secondary_contact_relationship != null && user.secondary_contact_relationship != '') {
                    $(this).html(user.secondary_contact_relationship);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.secondary-contact-phone1').each(function () {
                if (user.secondary_contact_phone1 != null && user.secondary_contact_phone1 != '') {
                    $(this).html(user.secondary_contact_phone1);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.secondary-contact-phone2').each(function () {
                if (user.secondary_contact_phone2 != null && user.secondary_contact_phone2 != '') {
                    $(this).html(user.secondary_contact_phone2);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.bank-name').each(function () {
                if (user.bank_name != null && user.bank_name != '') {
                    $(this).html(user.bank_name);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.bank-account-number').each(function () {
                if (user.bank_account_number != null && user.bank_account_number != '') {
                    $(this).html(user.bank_account_number);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.ifsc-code').each(function () {
                if (user.ifsc_code != null && user.ifsc_code != '') {
                    $(this).html(user.ifsc_code);
                } else {
                    $(this).html('Not Provided');
                };
            });

            $('.pan-number').each(function () {
                if (user.pan_number != null && user.pan_number != '') {
                    $(this).html(user.pan_number);
                } else {
                    $(this).html('Not Provided');
                };
            });
            
            $('#family-info').html('')
            if (user.family_member_data && Array.isArray(user.family_member_data)) {
                user.family_member_data.forEach(function (family_member) {
                    var newRow = `<tr>
                        <td class="border-0">Family Member</td>
                        <td class="border-0">${family_member.name}</td>
                    </tr>
                    <tr>
                        <td class="border-0">Relationship</td>
                        <td class="border-0">${family_member.relationship}</td>
                    </tr>
                    <tr>
                        <td class="border-0">Date of Birth</td>
                        <td class="border-0">${family_member.date_of_birth}</td>
                    </tr>
                    <tr>
                        <td>Phone</td>
                        <td>${family_member.phone}</td>
                    </tr>`
                    $('#family-info').append(newRow)
                });
            } else {
                $('#family-info').html('')
            }

            $('#education-info').html('')
            if (user.educational_information_data && Array.isArray(user.educational_information_data)) {
                user.educational_information_data.forEach(function (educational_info) {
                    var newRow = `<tr>
                        <td class="border-0">Institution</td>
                        <td class="border-0">${educational_info.institution}</td>
                    </tr>
                    <tr>
                        <td class="border-0">Course</td>
                        <td class="border-0">${educational_info.course}</td>
                    </tr>
                    <tr>
                        <td class="border-0">Started Year</td>
                        <td class="border-0">${educational_info.started_year}</td>
                    </tr>
                    <tr>
                        <td>Completed Year</td>
                        <td>${educational_info.completed_year}</td>
                    </tr>`
                    $('#education-info').append(newRow)
                })
            } else {
                $('#education-info').html('')
            }

            $('#experience-info').html('')
            if (user.experience_data && Array.isArray(user.experience_data)) {
                user.experience_data.forEach(function (experience) {
                    var completed_month_and_year = ''
                    if (experience.completed_month_and_year != null && experience.completed_month_and_year != '') {
                        completed_month_and_year = experience.completed_month_and_year
                    } else {
                        completed_month_and_year = 'Present'
                    }
                    var newRow = `<tr>
                        <td class="border-0">Designation</td>
                        <td class="border-0">${experience.designation}</td>
                    </tr>
                    <tr>
                        <td class="border-0">Company</td>
                        <td class="border-0">${experience.company}</td>
                    </tr>
                    <tr>
                        <td class="border-0">Started Month and Year</td>
                        <td class="border-0">${experience.started_month_and_year}</td>
                    </tr>
                    <tr>
                        <td>Completed Month and Year</td>
                        <td>${completed_month_and_year}</td>
                    </tr>`
                    $('#experience-info').append(newRow)
                })
            } else {
                $('#experience-info').html('')
            }

        },
        error: function (error) {
            console.error('Error: ', error);
        }
    })
}