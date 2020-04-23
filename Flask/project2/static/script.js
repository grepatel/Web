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
    })