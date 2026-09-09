import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import router.user_api, router.todos_api, router.user_web, router.todos_web
from utils import *


app = FastAPI()

app.include_router(router.user_api.router)
app.include_router(router.todos_api.router)
app.include_router(router.user_web.router)
app.include_router(router.todos_web.router)

app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/api/health_check")
async def health_check():
    return {"status": "ok"}


@app.get("/{html_filename:path}.html")
async def render_static_html_pages(html_filename: str):
    file_address = os.path.join("static/pages", f"{html_filename}.html")
    if os.path.exists(file_address):
        return FileResponse(file_address)
    return status_response_error(404, "Page not found")