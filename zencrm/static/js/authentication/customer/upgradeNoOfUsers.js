var noOfUsersInput = document.getElementById('no_of_users_input')
var current_no_users = noOfUsersInput.value

function manageNoOfUsers(inputValue, amountPerIndividual) {
    var new_no_users = inputValue;
    var difference = new_no_users - current_no_users    

    document.getElementById('user-upgrade-details').style.display = 'none'
    document.getElementById('no_of_user_btn_section').style.display = 'none'

    if (difference > 0) {
        document.getElementById('no-of-users-submit-btn').innerHTML = 'Pay and Upgrade'
        document.getElementById('no_of_user_btn_section').style.display = 'block'        
        document.getElementById('payable-amount').innerHTML = difference + ' * ' + amountPerIndividual + ' = ' + difference * amountPerIndividual
        document.getElementById('user-upgrade-details').style.display = 'block'
    } else if (difference < 0) {
        document.getElementById('no-of-users-submit-btn').innerHTML = 'Downgrade'
        document.getElementById('no_of_user_btn_section').style.display = 'block'        
    }

    if (inputValue < 1) {
        noOfUsersInput.value = 1;
    }
}