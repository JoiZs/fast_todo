import os
import uvicorn
import db_operate
from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()
load_dotenv('./.env.local')
dbi = db_operate.DbInstance(os.getenv("MONGODB_URL"))

@app.get("/")
async def root():
    await dbi.ping_server()
    return {"message":"hello"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=4000, reload=True)