let forgotPasswordSubmitBtn = document.getElementById('forgot-password-submit-btn');
var emailInput = document.getElementById('email-input');

forgotPasswordSubmitBtn.setAttribute('disabled', true)

emailInput.addEventListener('input', function() {

    var emailValue = emailInput.value

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const isValidEmail = emailRegex.test(emailValue);

    if (emailValue != null && emailValue != '' && isValidEmail) {
        forgotPasswordSubmitBtn.removeAttribute('disabled');
    } else {
        forgotPasswordSubmitBtn.setAttribute('disabled', true);
    };

});

function forgotPassword () {
    var resetPasswordModal = new bootstrap.Modal(document.getElementById('reset-password-modal'));
    var emailValue = emailInput.value;

    forgotPasswordSubmitBtn.setAttribute('disabled', true);

    $.ajax({
        type: 'POST',
        url: '/authentication/forgot_password/',
        dataType: 'json',
        data: {
            'email': emailValue
        },
        success: function (data) {
            resetPassword();
            resetPasswordModal.show();
            $('#password-reset-form').prop('action', '/authentication/reset_password/' + emailValue);
            startCountdown(300, document.getElementById('timer'), document.getElementById('resend-otp'));
            // OTP for resetting your password has been forwarded to your email         
        },
        error: function (error) {
            $('#invalid-email').html('Invalid email address. Please check your email and try again.')
            $('#email-input').focus();
            $('#email-input').addClass('border-danger');
            console.log('Error: ', error)
            console.log('Invalid email address.')
        },
    });
};


function resetPassword() {

    let CancelforgotPasswordBtn = document.getElementById('forgot-password-cancel-btn')
    
    CancelforgotPasswordBtn.click();
}