function openMessage(mode){
    var my_message = document.getElementById(`my-message-${mode}`);

    if (my_message.classList.contains('active')){
        my_message.classList.remove('active');
    }
    else{
        my_message.classList.add('active');
    }

    var my_profiles = document.querySelectorAll('[id^="my-profile"]');
    for (var x = 0; x < my_profiles; x++){
        if (my_profiles[x].classList.contains('active')){
            my_profiles[x].classList.remove('active');
        }
    }

    var my_notifs = document.querySelectorAll('[id^="my-notification"]');
    for (var x = 0; x < my_notifs.length; x++) {
        if (my_notifs[x].classList.contains('active')) {
        my_notifs[x].classList.remove('active');
        }
    }
}


function openNotification(mode){
    var my_notif = document.getElementById(`my-notification-${mode}`);

    if (my_notif.classList.contains('active')){
        my_notif.classList.remove('active');
    }
    else{
        my_notif.classList.add('active');
    }

    var my_profiles = document.querySelectorAll('[id^="my-profile"]');
    for (var x = 0; x < my_profiles; x++){
        if (my_profiles[x].classList.contains('active')){
            my_profiles[x].classList.remove('active');
        }
    }

    var my_messages = document.querySelectorAll('[id^="my-message"]');
    for (var x = 0; x < my_messages.length; x++) {
        if (my_messages[x].classList.contains('active')) {
            my_messages[x].classList.remove('active');
        }
    }
}

function openProfile(mode) {
    var my_profile = document.getElementById(`my-profile-${mode}`);
    
    if (my_profile.classList.contains('active')){
        my_profile.classList.remove('active');
    }
    else{
        my_profile.classList.add('active');
    }
        

    var my_notifs = document.querySelectorAll('[id^="my-notification"]');
    for (var x = 0; x < my_notifs.length; x++) {
        if (my_notifs[x].classList.contains('active')) {
            my_notifs[x].classList.remove('active');
        }
    }

    var my_messages = document.querySelectorAll('[id^="my-message"]');
    for (var x = 0; x < my_messages.length; x++) {
        if (my_messages[x].classList.contains('active')) {
            my_messages[x].classList.remove('active');
        }
    }
}