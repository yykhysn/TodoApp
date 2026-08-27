from fastapi import FastAPI

import router.user_api, router.todos_api, router.user_web



app = FastAPI()

app.include_router(router.user_api.router)
app.include_router(router.todos_api.router)


@app.get("/health_check")
async def health_check():
    return {"status": "ok"}