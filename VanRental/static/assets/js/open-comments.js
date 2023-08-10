
function openAllComments(id){
    var all_user_comments = document.querySelectorAll(`[id^="${id}"]`);
    for (var x = 0; x < all_user_comments.length; x++){
        console.log(all_user_comments[x])
        all_user_comments[x].style.display = 'block';
    }

    var open_btn = document.getElementById(`open-comments${id}`)
    open_btn.style.display = 'none';
    
    var hide_btn = document.getElementById(`hide-comments${id}`)
    hide_btn.style.display = 'block';

}

function hideAllComments(id){
    var all_user_comments = document.querySelectorAll(`[id^="${id}"]`);
    for (var x = 0; x < all_user_comments.length; x++){
        if (x < 3){
            all_user_comments[x].style.display = 'block';
        }
        else{
            all_user_comments[x].style.display = 'none';
        }
    }

    var open_btn = document.getElementById(`open-comments${id}`)
    open_btn.style.display = 'block';
    
    var hide_btn = document.getElementById(`hide-comments${id}`)
    hide_btn.style.display = 'none';
}