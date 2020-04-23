if(!localStorage.getItem('chatUserName'))
    localStorage.setItem('chatUserName','');

    document.addEventListener('DOMContentLoaded',() =>
    {

        document.querySelector('button').onclick = () =>
        {

            let chatName = document.getElementById('chatUserName').value;
            localStorage.setItem('chatUserName',chatName);
            document.querySelector('#msg').innerHTML = 'Hello ' + chatName + '!!';
        }

    var socket = io();
    socket.on('connect', function() {

        socket.emit('my event', {data: 'I\'m connected!'});
        document.querySelector('#btnSendMsg').onclick = () =>
        {
                const msg = document.querySelector('#txtMsg').value;
                socket.emit('send message',{'message':msg});
        }
    });
    })