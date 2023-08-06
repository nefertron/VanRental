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
}