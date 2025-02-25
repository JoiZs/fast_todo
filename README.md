# fast_todo

python restapi todo app > fastapi, mongodb, motor, pydantic

## Libries to install

```python
pip install uvicorn fastapi motor dotenv pydantic
```

## Steps to run development server

1. Initialize mongodb container using Docker
2. Run uvicorn local server - `python3 main.py`

## Environment Variables

    create a .env.local file inside the working directory with the following variables.

    1. MONGO_UNAME - user name of mongodb server
    2. MONGO_PW - password
    3. MONGODB_URL - mongodb uri(eg. "mongodb://{username}:{password}@localhost:27017/?authSource=admin")

## Setup MongoDB database using Docker

**Pulling mongodb image and initializing a container.**

```sh
- docker compose --env-file .env.local -f .\mongodb.docker-compose.yml up -d
- [+] Running 1/1
Container fast_todo-mongo-1  Started
```

**Check for the mongodb container**

```sh
- docker ps
- CONTAINER ID   IMAGE      COMMAND                  CREATED          STATUS         PORTS                      NAMES
c5af8b2ba89d mongo "docker-entrypoint.s…" 10 seconds ago Up 2 seconds 0.0.0.0:27017->27017/tcp fast_todo-mongo-1
815dfb9287a3   mongo-express   "/sbin/tini -- /dock…"   8 seconds ago   Up 1 second    0.0.0.0:8081->8081/tcp     fast_todo-mongo-express-1
```

**Enable Mongodb Authentication** - (_In case of authentication err..._)

```sh
- docker exec -it mongodb mongosh -u {MONGODB_UNAME} -p {MONGODB_PW} --authenticationDatabase admin
- test> db.runCommand({connectionStatus: 1})
```

`**:: -f for file location of docker-compose, & -d for running in detach mode**`

## Todo database Model

```py
class Task(BaseModel):
    title: str
    description: str
    completed: bool = False
```

## RestAPI Requests

**api routes** - by default, local server is running at: [localhost:4000](localhost:4000/)

1. **GET** - "/" (**Ping Request to the database**)
2. **GET** - "/tasks/{task_id}" (**Retrieving one task**)
3. **GET** - "/tasks" (**Retrieving all tasks**)
4. **POST** - "/create" (**creating a new task**)
5. **PUT** - "/tasks/{task_id}" (**updating a new task**)
6. **DELETE** - "/tasks/{task_id}" (**deleting a task**)

## Demo

Ping test using Postman.
![Pingtest](./public/pingtest.png)
