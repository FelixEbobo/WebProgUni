firstElem = document.getElementById("chislo")
Result = document.getElementById("Result")

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
