if(!localStorage.getItem('chatUserName'))
    localStorage.setItem('chatUserName','');
else
{
    document.querySelector('#msg').innerHTML = 'Hello ' + if(!localStorage.getItem('chatUserName')) + '!!';
    document.querySelector('#frmChatName').style.display='none';
}


    document.addEventListener('DOMContentLoaded',() =>
    {

        document.querySelector('button').onclick = () =>
        {

            let chatName = document.getElementById('chatUserName').value;
            localStorage.setItem('chatUserName',chatName);
            document.querySelector('#msg').innerHTML = 'Hello ' + chatName + '!!';
        }
    })