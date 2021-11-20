login = document.getElementById("login")
password = document.getElementById("password")

text_box = document.getElementById("message")
chat_stack = document.getElementById("chat-col")

LoginRequest = () => {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/login")
    xhr.setRequestHeader("Content-Type", "application/json")
    let data = {
        "username": login.value,
        "password": password.value
    }
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4 && xhr.status == 200)
        {
            document.location.reload()
        }
        if (xhr.readyState == 4 && xhr.status == 400) {
            alert("login failed!")
            return
        }
    };
    xhr.send(JSON.stringify(data))
}

LogoutRequest = () => {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/logout", true)
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4 && xhr.status == 200)
        {
            document.location.reload()
        }
    };
    xhr.send()
}

MessageRequest = () => {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/message", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    let data = {
        "message": text_box.value,
    }
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4 && xhr.status == 200)
        {
            RenderRequest()
        }
    };
    xhr.send(JSON.stringify(data))
    text_box.value = '';
}

RenderRequest = () => {
    fetch("/message")
        .then(function(response) {
            return response.json()
        })
        .then(function(jsonResponse) {
            chat_stack.innerHTML = ''
            let msg = document.createElement('div')
            msg.className = "row row-custom"
            for (let item of jsonResponse['list']) {
                msg.innerHTML = item['user'] + " : " + item['msg_text']
                chat_stack.appendChild(msg)
            }
        });
}

function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    else
    {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = dc.length;
        }
    }
    // because unescape has been deprecated, replaced with decodeURI
    //return unescape(dc.substring(begin + prefix.length, end));
    return decodeURI(dc.substring(begin + prefix.length, end));
} 

if (getCookie('token') != null) {
    RenderRequest()
}