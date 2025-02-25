from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskResponse(Task):
    id: str


# MongoDB Model -> Pydantic Model
def serialize_task(task) -> TaskResponse:
    return TaskResponse(id=str(task["_id"]), title=task["title"], description=task["description"], completed=task["completed"])


