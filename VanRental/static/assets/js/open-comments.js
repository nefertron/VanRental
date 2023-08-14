
function openAllComments(id){
    console.log(id)
    var all_user_comments = document.querySelectorAll(`[id^="${id}"]`);
    console.log(all_user_comments.length)

    for (var x = 0; x < all_user_comments.length; x++){
        console.log(all_user_comments[x])
        all_user_comments[x].style.display = '';
    }

    var open_btn = document.getElementById(`open-comments_${id}`)
    open_btn.style.display = 'none';
    
    var hide_btn = document.getElementById(`hide-comments_${id}`)
    hide_btn.style.display = '';

}

function hideAllComments(id){
    var all_user_comments = document.querySelectorAll(`[id^="${id}"]`);
    for (var x = 0; x < all_user_comments.length; x++){
        if (x < 1){
            all_user_comments[x].style.display = '';
        }
        else{
            all_user_comments[x].style.display = 'none';
        }
    }

    var open_btn = document.getElementById(`open-comments_${id}`)
    open_btn.style.display = '';
    
    var hide_btn = document.getElementById(`hide-comments_${id}`)
    hide_btn.style.display = 'none';
}