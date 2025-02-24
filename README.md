# fast_todo

## Environment Variables

    create a .env.local file inside the working directory with the following variables.

    1. MONGO_UNAME - user name of mongodb server
    2. MONGO_PW - password

## Setup MongoDB database using Docker

**Pulling mongodb image and initializing a container.**

```$
- docker compose --env-file .env.local -f .\mongodb.docker-compose.yml up -d
- [+] Running 1/1
Container fast_todo-mongo-1  Started
```

**Check for the mongodb container**

```$
- docker ps
- CONTAINER ID   IMAGE      COMMAND                  CREATED          STATUS         PORTS                      NAMES
c5af8b2ba89d mongo "docker-entrypoint.s…" 10 seconds ago Up 2 seconds 0.0.0.0:27017->27017/tcp fast_todo-mongo-1
815dfb9287a3   mongo-express   "/sbin/tini -- /dock…"   8 seconds ago   Up 1 second    0.0.0.0:8081->8081/tcp     fast_todo-mongo-express-1
```

**Enable Mongodb Authentication**

```$
- docker exec -it mongodb mongosh -u {MONGODB_UNAME} -p {MONGODB_PW} --authenticationDatabase admin
- test> db.runCommand({connectionStatus: 1})
```

`**Note: -f for file location of docker-compose, & -d for running in detach mode**`
