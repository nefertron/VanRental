const listItems = document.querySelectorAll('.custom-button');
            
listItems.forEach(item => {
    item.addEventListener('click', function(event) {
    const id_of_notif = item.dataset.message; // Get the message from the <p> tag
    
    fetch(`open/notification/${id_of_notif}/`)
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

            var modal_footer = document.getElementById('modal-footer');
            modal_footer.textContent = `Date Recorded : ${date_recorded} || ID : ${notification_id}`
        })
        .catch(error => {
            console.error("Error:", error);
        });
    
    });
});