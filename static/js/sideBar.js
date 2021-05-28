$(document).ready(function () {
    console.log('페이지가 로딩되었습니다.');
    $('#openNav').click(function () {
        // alert('사이드바를 엽니다.');
        $('#nav-sub').fadeIn(500);
    })
    $('#closeNav').click(function () {
        // alert('사이드바를 닫습니다.');
        $('#nav-sub').fadeOut(500);
    })
});

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.body.style.backgroundColor = "rgba(0,0,0,0.6)";
}
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.body.style.backgroundColor = "white";
}