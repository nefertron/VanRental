const listItems = document.querySelectorAll('.notification-button');
            
listItems.forEach(item => {
    item.addEventListener('click', function(event) {
    const id_of_notif = item.dataset.message; // Get the message from the <p> tag
    
    
    

    fetch(`http://127.0.0.1:8000/open/notification/${id_of_notif}/`)
        .then(response => response.json())
        .then(data => {
            const message = data['messages'];
            const notification = data['message'];
            const notification_id = data['notification_id'];
            const date_recorded = data['date_recorded'];

            if (message !== undefined){
                var modalOverlay = document.getElementById('seen_message');
                var modal = modalOverlay.querySelector(".modal");
                modalOverlay.classList.add("active");
                modal.classList.add("active");
            }


            var modal_title_holder = document.getElementById('modal-title-holder');
            modal_title_holder.textContent = message

            var modal_body_holder = document.getElementById('modal-body-holder');
            modal_body_holder.textContent = notification


            // CONVERT THE DATE
            const to_convert_date = new Date(date_recorded)

            var months = [
                "Jan", "Feb", "Mar",
                "Apr", "May", "Jun",
                "Jul", "Aug", "Sep",
                "Oct", "Nov", "Dec"
            ];

            console.log('to conver', to_convert_date)
            var monthStr = months[to_convert_date.getMonth()]
            var day = to_convert_date.getDate()
            var year = to_convert_date.getFullYear()
            var hour = to_convert_date.getHours()
            var minute = to_convert_date.getMinutes()

            let ampm;
            if (hour > 12){
                ampm = 'pm'
                hour -= 12;
                if (hour < 10){
                    hour = `0${hour}`
                }
            }
            else{
                if (hour == 0){
                    hour = 12
                }
                else{
                    if (hour < 10){
                        hour = `0${hour}`
                    }
                }
                ampm = 'am'
            }

            if (minute < 10){
                minute  = `0${minute}`
            }

            var formatted_date = `${monthStr} ${day}, ${year}  ${hour} : ${minute} ${ampm}`
            // CONVERT THE DATE
            var modal_footer = document.getElementById('modal-footer');
            modal_footer.textContent = `Date Recorded : ${formatted_date}\n\nID : ${notification_id}`

            console.log('hello')
            const all_notifications = document.querySelectorAll(`[id^="notification_${id_of_notif}"]`);
            for (var x = 0; x < all_notifications.length; x++){
                all_notifications[x].removeAttribute('style');
                console.log(x)
            }
            
        })
        .catch(error => {
            console.error("Error:", error);
        });
    
    });
});