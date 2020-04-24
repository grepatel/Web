
document.addEventListener('DOMContentLoaded',() =>
{
        if(!localStorage.getItem('username'))
        {
            localStorage.setItem('username','');
            document.querySelector('#frmChatName').style.display='block';
            document.querySelector('#btnChangeChatName').style.display='none';
        }
        else
        {

            document.querySelector('#msg').innerHTML = "Hello " + localStorage.getItem('username') + "!!";
            document.querySelector('#frmChatName').style.display='none';
            document.querySelector('#btnChangeChatName').style.display='block';
        }

        if(!localStorage.getItem('chatroomname'))
        {
            const chatroomName='Default';
            localStorage.setItem('chatroomname',chatroomName);
            AddListItem('#lstChatroom',chatroomName);
        }

        document.querySelector('#btnChatName').onclick = () =>
        {

            let chatName = document.getElementById('chatUserName').value;
            localStorage.setItem('username',chatName);
            document.querySelector('#msg').innerHTML = "Hello " + chatName + "!!";
            document.querySelector('#frmChatName').style.display='none';
            document.querySelector('#btnChangeChatName').style.display='block';

        }

        document.querySelector('#btnChangeChatName').onclick = () =>
        {
            document.querySelector('#frmChatName').style.display='block';
            document.querySelector('#btnChangeChatName').style.display='none';
        }

        document.querySelector("#btnCreateChatroom").onclick = () =>
        {
            chatroomName=document.querySelector('#txtChatroomName').value;
            AddListItem('#lstChatroom',chatroomName);
        }

    var socket = io();
    socket.on('connect', function()
    {

        document.querySelector('#btnSendMsg').onclick = () =>
        {
                const msg = localStorage.getItem('username') + ": " + document.querySelector('#txtMsg').value + '\n';
                socket.emit('send message',{'message':msg});
                document.querySelector('#txtMsg').value='';
        };
    });

    socket.on('broadcast',data =>
    {
          document.querySelector('#txtChatWindow').value=data.chatText;
    });
});

function AddListItem(ulId,liText)
{
                var ul = document.querySelector(ulId);
                 var li = document.createElement('li');
                li.appendChild(document.createTextNode(liText));
                li.setAttribute('id', liText);
                li.setAttribute('class','list-group-item')
                ul.appendChild(li);
}
