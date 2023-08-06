document.getElementById('birthdate-input').addEventListener('input', function() {
    var inputDate = new Date(this.value);
    var currentDate = new Date();
    
    console.log(inputDate)
    console.log(currentDate)

    if (inputDate > currentDate) {
        alert("Please enter a valid birth date");
        this.value = ''
    } else {
        this.setCustomValidity("");
    }
});