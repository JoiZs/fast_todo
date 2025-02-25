import os
import uvicorn
import db_operate
from fastapi import FastAPI, Response
from dotenv import load_dotenv
from db_model import Task

app = FastAPI()
load_dotenv('./.env.local')
dbi = db_operate.DbInstance(os.getenv("MONGODB_URL"))

@app.get("/")
async def root(response: Response):
    result = await dbi.ping_server()
    response.status_code = result.status
    return result

@app.get("/tasks/{task_id}")
async def onetask(task_id: str, response: Response):
    result = await dbi.getTask(task_id=task_id)
    response.status_code = result.status
    return result

@app.delete("/tasks/{task_id}")
async def onetask(task_id: str, response: Response):
    result = await dbi.delTask(task_id=task_id)
    response.status_code = result.status
    return result

@app.post("/create")
async def onetask(task: Task, response: Response):
    result = await dbi.createTask(task)
    response.status_code = result.status
    return result

@app.get("/tasks/")
async def alltasks(response: Response):
    result = await dbi.getTasks()
    response.status_code = result.status
    return result

@app.put("/tasks/{task_id}")
async def updatetask(task_id:str,task:Task, response: Response):
    result = await dbi.updateTask(task_id=task_id, task=task)
    response.status_code = result.status
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=4000, reload=True)
