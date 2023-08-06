function openModal(overlayId) {
    const modalOverlay = document.getElementById(overlayId);
    const modal = modalOverlay.querySelector(".modal");
    modalOverlay.classList.add("active");
    modal.classList.add("active");
}

function closeModal(overlayId) {
    const modalOverlay = document.getElementById(overlayId);
    const modal = modalOverlay.querySelector(".modal");
    modalOverlay.classList.remove("active");
    modal.classList.remove("active");
}



function openPendingDriverModal(button) {
    
    var userId = button.getAttribute('data-userid');
    var email = undefined;

    fetch(`pending-driver-info/${userId}/`)
        .then(response => response.json())
        .then(data => {
            email = `${data.email}`;

            if (email !== undefined){
                var modalOverlay = document.getElementById('pending_driver');
                var modal = modalOverlay.querySelector(".modal");
                modalOverlay.classList.add("active");
                modal.classList.add("active");
            }

            var modal_title_holder = document.getElementById('modal-title-holder');
            modal_title_holder.textContent = `Are you sure you want to approve this account ? ${email}`

            const send_email_input_field = document.querySelector('input[name="send_email_to_this_id"]');
            send_email_input_field.value = data.id

        })
        .catch(error => {
            console.error("Error:", error);
        });
    

    
    
    // var userId = button.getAttribute('data-userid');
    // console.log("Opening modal for User ID:", userId);




    // var apiUrl = `approve-pending-driver/${userId}/`;
    
    // fetch(apiUrl)
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log("Response from the backend:", data.message);
    //     })
    //     .catch(error => {
    //         console.error("Error:", error);
    //     });
}

function closePendingDriverModal() {
    var modalOverlay = document.getElementById('pending_driver');
    var modal = modalOverlay.querySelector(".modal");
    modalOverlay.classList.remove("active");
    modal.classList.remove("active");
}