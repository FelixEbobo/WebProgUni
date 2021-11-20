from ctypes import resize
import time
from math import sqrt
from aiohttp import web
import asyncio
from hashlib import md5
import json

async def css_handler(request: web.Request):
    cookies = request.cookies

    file = "default_theme.css"
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
    with open("index.html", "r", encoding="utf-8") as f:
        html_body = f.read()

    response.text = html_body

    return response

def factors(n: int):
    j = 2
    while n > 1:
        for i in range(j, int(n + 1)):
            if n % i == 0:
                n /= i 
                yield i
                break

async def calculate_handler(request: web.Request):
    response = web.Response(
        content_type="text/json"
    )
    

    return response

async def init_app(loop):
    app = web.Application(loop=loop, middlewares=[])
    app.router.add_get('/themed.css', css_handler)
    app.router.add_get('/', index_handler)
    app.router.add_get('/index.js', js_handler)
    app.router.add_post('/calculate', )
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
    print()