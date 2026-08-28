from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import router.user_api, router.todos_api, router.user_web



app = FastAPI()

app.include_router(router.user_api.router)
app.include_router(router.todos_api.router)
app.include_router(router.user_web.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/health_check")
async def health_check():
    return {"status": "ok"}