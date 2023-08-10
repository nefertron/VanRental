

function dateChecker(input_id){
    var input_date = document.getElementById(input_id);
    var inputDate = new Date(input_date.value);
    var currentDate = new Date();
    
    if (inputDate < currentDate) {
        alert("Please enter a valid birth date. Prefarably, use the calendar button.");
        input_date.value = ''
    } else {
        input_date.setCustomValidity("");
    }
};
