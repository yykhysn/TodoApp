from fastapi import FastAPI

import router.auth, router.to_do_app



app = FastAPI()

app.include_router(router.auth.router)
app.include_router(router.to_do_app.router)