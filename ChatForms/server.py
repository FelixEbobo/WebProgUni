import time
from typing import DefaultDict
from aiohttp import web
from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_response import Response
import aiomysql
from jinja2 import Environment, FileSystemLoader
import asyncio
from hashlib import md5
import json
import shlex

ENV = Environment(loader=FileSystemLoader('templates'))

MYSQL_PARAMS = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "h4wPDw",
    "db": "gyoubu_masataka_oniwa"
}

def pass_hash(username: str, password: str) -> str:
    pass_str = username + password + "jkldsafu879v82h3nkl"
    return md5(pass_str.encode("utf-8")).hexdigest()

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
    cookies = request.cookies
    if cookies.get('token'):
        msg_list = []

        conn = await mysql_connect()
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute("SELECT users.name AS user, msg_text, msg_date FROM messages JOIN users ON users.id = messages.user ORDER BY msg_date ASC")
        messages = await cur.fetchall()

        tmpl = ENV.get_template('message.tmpl')
        print(messages)
        for message in messages:
            msg_list.append(tmpl.render(**message))

        tmpl = ENV.get_template('index_logged.html')
        response.text = tmpl.render(chat_messages=msg_list)
    else:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            response.text = f.read()

    return response

async def test_db(request: web.Request):

    conn = await mysql_connect()
    cur = await conn.cursor(aiomysql.DictCursor)
    cur: aiomysql.DictCursor

    await cur.execute("SELECT * FROM test_var")
    r = await cur.fetchall()
    print(r)

    return web.Response(
        content_type="application/json",
        text=json.dumps(r)
    )

async def login_handler(request: web.Request):
    data = await request.post()
    login = (data['login'])
    password = pass_hash(data['login'], data['password'])
    conn = await mysql_connect()
    cur = await conn.cursor(aiomysql.DictCursor)
    await cur.execute(f"SELECT token FROM users WHERE name = '{login}' AND password = '{password}'")
    r = await cur.fetchone()
    if r:
        response = web.HTTPFound('/')
        response.set_cookie('token', r['token'])
        return response

    return web.HTTPNotFound()

async def message_handler(request: web.Request):

    cookies = request.cookies
    token = cookies['token']
    data = await request.post()
    if not data.get('message'):
        return web.HTTPFound('/')

    conn = await mysql_connect()
    cur = await conn.cursor(aiomysql.DictCursor)
    await cur.execute(f"SELECT id FROM users WHERE token = '{token}'")
    r = await cur.fetchone()
    user_id = r['id']
    msg = shlex.quote(data['message'])
    await cur.execute(f"INSERT INTO messages (user, msg_text) VALUES ('{user_id}', {msg})")
    await conn.commit()

    return web.HTTPFound('/')

async def logout_handler(request: web.Request):
    response = web.HTTPFound('/')
    response.del_cookie('token')
    return response

async def init_app(loop):
    app = web.Application(loop=loop, middlewares=[])
    app.router.add_get('/', index_handler)
    app.router.add_get('/index.js', js_handler)
    app.router.add_get('/test_db', test_db)
    app.router.add_post('/login', login_handler)
    app.router.add_post('/message', message_handler)
    app.router.add_post('/logout', logout_handler)
    return app

async def mysql_connect() -> aiomysql.Connection:
    conn = await aiomysql.connect(**MYSQL_PARAMS)
    return conn

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