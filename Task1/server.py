import time
from aiohttp import web
import asyncio
from hashlib import md5
import json

def get_users():
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.loads(f.read())
    return users

def write_users(write_data):
    with open("users.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(write_data))

def pass_hash(username: str, password: str) -> str:
    pass_str = username + password + "jkldsafu879v82h3nkl"
    return md5(pass_str.encode("utf-8")).hexdigest()

async def css_handler(request: web.Request):
    cookies = request.cookies

    if cookies.get("theme"):
        theme = cookies["theme"]
        if theme == "default":
            file = "default_theme.css"
        elif theme == "pink":
            file = "pink_theme.css"

    response = web.Response(
        content_type="text/css"
    )

    with open(file, "r", encoding="utf-8") as f:
        html_body = f.read()

    response.text = html_body

    return response

async def js_handler(request: web.Request):

    with open("index.js", "r", encoding="utf-8") as f:
        response = web.Response(
            content_type="text/javascript",
            text=f.read()
        )

    return response

async def index_handler(request: web.Request):
    response = web.Response(
        content_type="text/html"
    )
    cookie = request.cookies
    if cookie.get("token"):
        token = cookie["token"]
        with open("index_logged.html", "r", encoding="utf-8") as f:
            html_body = f.read()
        users = get_users()
        for user in users["users"]:
            user: dict
            if user.get("token") == token:
                html_body = html_body.replace("||user||", user["username"])
    else:
        with open("index.html", "r", encoding="utf-8") as f:
            html_body = f.read()

    response.text = html_body

    return response

async def login_handler(request: web.Request):
    data = await request.json()

    login = data["username"]
    pass_str = pass_hash(login, data["password"])
    users = get_users()
    for user in users["users"]:
        if user["username"] == login and user["password"] == pass_str:
            cookie = str(time.time()) + login + pass_str
            cookie = md5(cookie.encode("utf-8")).hexdigest()
            response = web.Response(text="granted")
            response.set_cookie("token", cookie)
            response.set_cookie("theme", user["theme"])
            user["token"] = cookie

            write_users(users)

            return response

    return web.Response(text="login failed", status=400)

async def logout_handler(request: web.Request):
    cookie = request.cookies
    response = web.Response()
    users = get_users()
    token = cookie["token"]
    for user in users["users"]:
        if user.get("token") == token:
            del user["token"]
            response.del_cookie("token")
            response.text = "ok"
    
    write_users(users)
    return response

async def register_handler(request: web.Request):
    data = await request.json()

    users = get_users()

    new_user = {
        "username": data["username"],
        "password": pass_hash(data["username"], data["password"]),
        "theme": request.cookies["theme"]
    }
    
    users["users"].append(new_user)
    write_users(users)
    
    return web.Response(text="ok")

async def theme_handler(request: web.Request):
    cookie = request.cookies
    if cookie.get("token"):
        token = cookie["token"]
        users = get_users()
        for user in users["users"]:
            if user.get("token") == token:
                user["theme"] = request.match_info["name"]
        
        write_users(users)

    response = web.Response(
        content_type="text/css"
    )
    response.set_cookie("theme", request.match_info['name'])
    if request.match_info['name'] == "pink":
        file = "pink_theme.css"
    elif request.match_info['name'] == "default":
        file = "default_theme.css"
    with open(file, "r", encoding="utf-8") as f:
        response.text = f.read()
    return response

async def init_app(loop):
    app = web.Application(loop=loop, middlewares=[])
    app.router.add_get('/themed.css', css_handler)
    app.router.add_get('/', index_handler)
    app.router.add_post('/login', login_handler)
    app.router.add_post('/logout', logout_handler)
    app.router.add_post('/register', register_handler)
    app.router.add_get('/theme/{name}', theme_handler)
    app.router.add_get('/index.js', js_handler)
    return app

def main():
    loop = asyncio.get_event_loop()
    try:
        web_app = loop.run_until_complete(init_app(loop))
        web.run_app(web_app, host='0.0.0.0', port=8081)
    except Exception as e:
        print('Error create server: %r' % e)
    finally:
        pass
    loop.close()

if __name__ == "__main__":
    main()