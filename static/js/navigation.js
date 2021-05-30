// window.onload = function () {
//     window.onscroll = function () { addScroll() };

//     function addScroll() {
//         if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
//             document.getElementsByClassName("header")[0].style.top = '-100px';
//             document.getElementsByClassName("nav")[0].style.top = '-100px';
//             console.log('네비 닫힘!');
//             var top = $(".header").offset();
//             console.log(top);
//         } else {
//             document.getElementsByClassName("header")[0].style.top = '0';
//             document.getElementsByClassName("nav")[0].style.top = '0';
//             console.log('네비 펼침!');
//             var top = $(".header").offset();
//             console.log(top);
//         }
//     }
// }
window.onload = function () {
    var prevScrollpos = window.pageYOffset;
    window.onscroll = function () { addScroll() };

    function addScroll() {
        var currentScrollPos = window.pageYOffset;
        if (prevScrollpos > currentScrollPos) {
            document.getElementsByClassName("header")[0].style.top = '0';
            document.getElementsByClassName("nav")[0].style.top = '0';
        } else {
            document.getElementsByClassName("header")[0].style.top = '-100px';
            document.getElementsByClassName("nav")[0].style.top = '-100px';
        }
        prevScrollpos = currentScrollPos;
    }

    $('.logo').click(function () {
        location.href = 'http://localhost:5000';
    })
}