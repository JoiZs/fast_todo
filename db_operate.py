from motor.motor_asyncio import AsyncIOMotorClient


class DbInstance:
    def __init__(self, server):
        self.client = AsyncIOMotorClient(server)
    
    async def ping_server(self):
        try:
            await self.client.admin.command("ping")
            print("Ping..")
        except Exception as e:
            print(e)
    
    

