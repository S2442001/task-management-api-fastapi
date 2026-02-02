from fastapi import FastAPI
from app.apis import auth, crud

app=FastAPI(title="TASK MANAGER API")

app.include_router(auth.router)
app.include_router(crud.router)