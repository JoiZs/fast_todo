from motor.motor_asyncio import AsyncIOMotorClient
from db_model import Task, TaskResponse, serialize_task
from pydantic import BaseModel
from fastapi import status
from bson import ObjectId, errors

class ResponseMsg(BaseModel):
    status: int
    message: str
    data: TaskResponse | list[TaskResponse] | None

class DbInstance:
    def __init__(self, server):
        self.client = AsyncIOMotorClient(server)
        self.db = self.client["todo"]
        self.collections = self.db["tasks"]
    
    async def ping_server(self):
        try:
            await self.client.admin.command("ping")
            return ResponseMsg(status=status.HTTP_200_OK, message="Ping...", data=None)
        except Exception as e:
            print(e)
            return ResponseMsg(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Err at connecting MongoDB...", data=None)
    

    # Create a task
    async def createTask(self, task: Task) -> TaskResponse:
        try:
            res = await self.collections.insert_one(task.dict())
            newTask = await self.collections.find_one({"_id":res.inserted_id})
            return ResponseMsg(status=status.HTTP_201_CREATED,message="Created a task.", data=serialize_task(newTask))
        except Exception as e:
            print(e)
            return ResponseMsg(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Error at creating a new task", data=None)

    # Get a task by id
    async def getTask(self, task_id: str):
        try:
            task = await self.collections.find_one({"_id":ObjectId(task_id)})
            if not task:
                return ResponseMsg(status=status.HTTP_404_NOT_FOUND,message="Task not found.", data=None)
            return ResponseMsg(status=status.HTTP_200_OK,message="Task exists.", data=serialize_task(task))
        except errors.InvalidId:
            return ResponseMsg(status=status.HTTP_400_BAD_REQUEST, message="Invalid task id.", data=None)
        except Exception as e:
            print(e)
            return ResponseMsg(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Error at retrieving a task.", data=None)

    # Retrieve all tasks
    async def getTasks(self):
        try:
            tasks = await self.collections.find().to_list(length=100)
            return ResponseMsg(status=status.HTTP_200_OK, message=f"Found {len(tasks)} tasks.", data=[serialize_task(t) for t in tasks])
        except Exception as e:
            print(e)
            return ResponseMsg(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Error at retrieving tasks.", data=None)

        
    # Delete a task by id
    async def delTask(self, task_id: str):
        try:
            task = await self.collections.delete_one({"_id":ObjectId(task_id)})
            if task.deleted_count == 0:
                return ResponseMsg(status=status.HTTP_404_NOT_FOUND,message="Task not found.", data=None)
            return ResponseMsg(status=status.HTTP_200_OK,message="Deleted a task.", data=None)
        except errors.InvalidId:
            return ResponseMsg(status=status.HTTP_400_BAD_REQUEST, message="Invalid task id.", data=None)
        except Exception as e:
            print(e)
            return ResponseMsg(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Error at retrieving a task.", data=None)
    
    # Update a task by id
    async def updateTask(self, task_id:str, task: Task):
        try:
            updatetask = await self.collections.update_one({"_id":ObjectId(task_id)},{
                "$set": task.dict()
            })
            if updatetask.modified_count ==0:    
                return ResponseMsg(status=status.HTTP_400_BAD_REQUEST, message="No task updated.", data=None)
            newResult = await self.collections.find_one({"_id": ObjectId(task_id)})
            return ResponseMsg(status=status.HTTP_200_OK, message="Updated the task..", data=serialize_task(newResult))
        except errors.InvalidId:
            return ResponseMsg(status=status.HTTP_400_BAD_REQUEST, message="Invalid task id.", data=None)
        except Exception as e:
            print(e)
            return ResponseMsg(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Error at retrieving a task.", data=None)
