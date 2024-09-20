from database_service.mysql_service import MySQLService
from database_service.lib.abcs.database_service_abc import DatabaseServiceABC
from sqlalchemy.orm import DeclarativeBase
from database_service.models.query_param import QueryParamsModel
from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')
class DatabaseService(Generic[T]):
    def __init__(self, schema: DeclarativeBase,  db: DatabaseServiceABC = MySQLService.get_instance()):
        self.db = db
        self.schema = schema
    
    def connect(self):
        self.db.connect()
    
    def disconnect(self):
        self.db.disconnect()
    
    def create_metadata(self):
        self.db.create_metadata()
    
    async def getOne(self, id: str) -> T:
        return await self.db.getOne(id, self.schema)

    async def getAll(self, query: QueryParamsModel) -> list[T]:
        return await self.db.getAll(query, self.schema)
    
    async def createOne(self, data: BaseModel) -> T:
        return await self.db.createOne(data, self.schema)
    
    async def updateOne(self, id: str, data: BaseModel) -> T:
        return await self.db.updateOne(id, data, self.schema)
    
    async def deleteOne(self, id: str):
        return await self.db.deleteOne(id, self.schema)
