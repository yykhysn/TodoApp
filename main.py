from fastapi import FastAPI

import router.user, router.todos



app = FastAPI()

app.include_router(router.user.router)
app.include_router(router.todos.router)