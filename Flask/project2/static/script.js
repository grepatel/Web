


document.addEventListener('DOMContentLoaded',() =>
{
        Load_Page();

        var socket = io();
        socket.on('connect', function()
        {
            document.querySelector('#btnSendMsg').onclick = () =>
            {
                    const chatroomName=localStorage.getItem('chatroomname');
                    const msg = '[' + new Date().toLocaleString() + '] ' + localStorage.getItem('username') + " : " + document.querySelector('#txtMsg').value + '\n';
                    socket.emit('send message',{'chatroom':chatroomName, 'message':msg});
                    document.querySelector('#txtMsg').value='';
            };
        });

        EventCallBacks(socket);

        SocketCallBacks(socket);

});


function Load_Page()
{
        if(!localStorage.getItem('username'))
        {
            localStorage.setItem('username','');
            document.querySelector('#frmChatName').style.display='block';
            document.querySelector('#btnChangeUsername').style.display='none';
        }
        else
        {

            document.querySelector('#msg').innerHTML = "Hello " + localStorage.getItem('username') + "!!";
            document.querySelector('#frmChatName').style.display='none';
            document.querySelector('#btnChangeUsername').style.display='block';
        }

        if(!localStorage.getItem('chatroomname'))
        {
            const chatroomName='Default';
            localStorage.setItem('chatroomname',chatroomName);
            AddListItem('#lstChatroom',chatroomName);
        }

        var chatrooms  = JSON.parse(document.querySelector('#serverChatObj').dataset.chatrooms);

        chatrooms.forEach(function(room) {
            AddListItem('#lstChatroom',room.name);
            })

        const chatroom = chatrooms.find( x => x.name ===localStorage.getItem('chatroomname'));
        document.querySelector('#txtChatWindow').value = chatroom?chatroom.text:"";
}

function EventCallBacks(socket)
{
        document.querySelector('#btnUsername').onclick = () =>
        {

            let chatName = document.getElementById('username').value;
            localStorage.setItem('username',chatName);
            document.querySelector('#msg').innerHTML = "Hello " + chatName + "!!";
            document.querySelector('#frmChatName').style.display='none';
            document.querySelector('#btnChangeUsername').style.display='block';

        }

        document.querySelector('#btnChangeUsername').onclick = () =>
        {
            document.querySelector('#frmChatName').style.display='block';
            document.querySelector('#btnChangeUsername').style.display='none';
        }

        document.querySelector("#btnCreateChatroom").onclick = () =>
        {
            const chatroomName=document.querySelector('#txtChatroomName').value;
            socket.emit('new chatroom',{'chatroom':chatroomName,'username':localStorage.getItem('username')});
            localStorage.setItem('chatroomname',chatroomName);
        }

        document.querySelectorAll('.nav-link').forEach( link =>
        {
            link.onclick  = () =>
            {
                loadChat(link.dataset.page);
                return false;
            }

        })
}

function SocketCallBacks(socket)
{

    socket.on('broadcast msg',data =>
    {
          document.querySelector('#txtChatWindow').value=data.text;
    });

    socket.on('broadcast chatroom',data =>
    {
          console.log("caught broadcast chatroom event");
          const chatroom = JSON.parse(data);
          console.log("caught broadcast chatroom event :: " + chatroom.name)
          AddListItem('#lstChatroom',chatroom.name);
    });
}

function loadChat(chatroomName)
{
    const request = new XMLHttpRequest();
    request.open('GET',`/${chatroomName}`);
    request.onload = () =>
    {
        document.querySelector('#txtChatWindow').value = request.responseText;
    };
    request.send();
}
function AddListItem(ulId,liText)
{
                var ul = document.querySelector(ulId);
                var li = document.createElement('a');
                li.appendChild(document.createTextNode(liText));
                li.setAttribute('id', liText);
                li.setAttribute('href','');
                li.setAttribute('data-page',liText);
                li.setAttribute('class','list-group-item list-group-item-action nav-link')
                ul.appendChild(li);
}
