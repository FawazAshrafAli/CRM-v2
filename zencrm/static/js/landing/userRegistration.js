function userRegistration() {
    var plan = document.getElementById('plan').value;
    var noOfUsers = document.getElementById('no_of_users').value;
    const ratePerPerson = 6000;
    var discount = 0

    if (plan >= 1) {
        discount = 0.04 + plan * 0.01;
    };    

    var totalAmount = noOfUsers * ratePerPerson * plan;
    if (totalAmount != null && totalAmount != 0) {
        document.getElementById("amount-details").style.display = 'block';
    } else {
        document.getElementById("amount-details").style.display = 'none';
    }

    var discountedAmount = Math.round(discount * totalAmount);
    
    var amoutPayable = totalAmount - discountedAmount;    

    document.getElementById('discount').innerHTML = '- &#8377; ' + discountedAmount;
    document.getElementById('total-amount').innerHTML = '&#8377; ' + totalAmount;
    document.getElementById('amount-payable').innerHTML = '&#8377; ' + amoutPayable;
}