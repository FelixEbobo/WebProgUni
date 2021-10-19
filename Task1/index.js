firstElem = document.getElementById("elementA")
secondElem = document.getElementById("elementB")
Operand = document.getElementById("OperSelect")
Result = document.getElementById("Result")

login = document.getElementById("loginUsername")
password = document.getElementById("loginPassword")

CalculateResult = () => {
    let a = Number.parseFloat(firstElem.value)
    let b = Number.parseFloat(secondElem.value)
    let c
    let oper = Operand.value
    if (Number.isNaN(a) || Number.isNaN(b)) {
        alert("Enter valid numbers!")
        return
    }
    switch(oper) {
        case '+': {
            c = a + b
            break
        }
        case '-': {
            c = a - b
            break
        }
        case '*': {
            c = a * b
            break
        }
        case '/': {
            if (b == 0) {
                alert("You can't divide on zero!")
                return
            }
            c = a / b
            break
        }
    }
    Result.value = c

}

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
    xhr.open("POST", "/logout")
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4 && xhr.status == 200)
        {
            document.location.reload()
        }
    };
    xhr.send()
}

RegisterRequest = () => {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/register")
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
    };
    xhr.send(JSON.stringify(data))
}

SetCookieReq = (a) => {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/theme/" + a)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send()
    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4 && xhr.status == 200)
        {
            document.location.reload()
        }
    };
}