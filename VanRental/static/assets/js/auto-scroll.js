var messageContainer = document.getElementById("msg-container");
messageContainer.scrollTop = messageContainer.scrollHeight;

document.addEventListener("DOMContentLoaded", function () {
    // Scroll to the form container
    var scrollToForm = document.getElementById("scroll-to-form");
    if (scrollToForm) {
        scrollToForm.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    }
});