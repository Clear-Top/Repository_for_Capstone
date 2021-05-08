window.onload = function () {
    alert('마우스이벤트호출');

    var btn1 = document.getElementById('button1');
    var btn2 = document.getElementById('button2');
    var hello = document.getElementsById('searchDisplay');
    var icon = document.getElementsByClassName('icon');

    icon.addEventListener('click',
        function () {
            alert('클릭');
        }
    );

    hello.addEventListener('mouseover',
        function () {
            this.innerHTML = 'hello';
        }
    );

    hello.addEventListener('mouseout',
        function () {
            this.innerHTML = 'bye';
        }
    );

    btn1.addEventListener('mouseover',
        function () {
            this.innerHTML = 'Excel 파일 불러오기';
        }
    );

    btn1.addEventListener('mouseout',
        function () {
            this.innerHTML = 'How to use';
            btn1.style.fontSize = 'x-large';
        }
    );

    btn2.addEventListener('mouseover',
        function () {
            this.innerHTML = 'Marker 켜기/끄기';
        }
    );

    btn2.addEventListener('mouseout',
        function () {
            this.innerHTML = 'How to use';
            btn1.style.fontSize = 'x-large';
        }
    );
}
