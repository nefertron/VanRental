function openSideBar(){

    var side_bar = document.getElementById('van-rental-sidebar')
    side_bar.classList.add('active')

    var open_sidebar_btn = document.getElementById('menu-btn').style.display = "none";
    var close_sidebar_btn = document.getElementById('close-menu-btn').style.display = "block";
}

function closeSideBar(){
    var side_bar = document.getElementById('van-rental-sidebar')
    side_bar.classList.remove('active')

    var open_sidebar_btn = document.getElementById('menu-btn').style.display = "block";
    var close_sidebar_btn = document.getElementById('close-menu-btn').style.display = "none";

}