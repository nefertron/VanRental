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
    var modalOverlay = document.getElementById('pending_driver');
    var modal = modalOverlay.querySelector(".modal");
    modalOverlay.classList.add("active");
    modal.classList.add("active");
    var userId = button.getAttribute('data-userid');
    console.log("Opening modal for User ID:", userId);


    var apiUrl = `approve-pending-driver/${userId}/`;

    // Data to be sent to the backend
    var data = {
        user_id: userId
    };

    // Fetch API POST request
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Handle the response from the backend (if needed)
            console.log("Response from the backend:", data);
            // You can perform further actions based on the response here.
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function closePendingDriverModal() {
    var modalOverlay = document.getElementById('pending_driver');
    var modal = modalOverlay.querySelector(".modal");
    modalOverlay.classList.remove("active");
    modal.classList.remove("active");
}