from database_service.lib.abcs.database_service_abc import DatabaseServiceABC
from database_service.models.query_param import QueryParamsModel
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declarative_base, Session, load_only, joinedload, exc
from sqlalchemy import create_engine, text
from pydantic import BaseModel
import os

class MySQLService(DatabaseServiceABC):
    instance = None
    def __init__(self) -> None:
        self.base = declarative_base()
        self.connect()

    def connect(self):
        print(os.getenv("DB_URL"))
        self.engine = create_engine(os.getenv("DB_URL", "localhost"))
        self.session: Session = sessionmaker(bind=self.engine, autoflush=True)()
        self.create_metadata()

    def disconnect(self):
        self.session.close()
        self.engine.dispose()
    
    def create_metadata(self):
        self.base.metadata.create_all(self.engine)
    
    @staticmethod
    def get_base() -> DeclarativeBase:
        return MySQLService.get_instance().base
    
    @staticmethod
    def get_instance():
        if MySQLService.instance is None:
            MySQLService.instance = MySQLService()
        return MySQLService.instance
        
    async def getOne(self, id: str, schema: DeclarativeBase):
        cursor = self.session.query(schema(id = id))
        return cursor.first()

    async def getAll(self, query: QueryParamsModel, schema: DeclarativeBase):
        cursor = self.session.query(schema)

        if query.selected_fields:
            columns = [getattr(schema, field) for field in query.selected_fields]
            cursor = cursor.options(load_only(*columns))
        
        if query.join_fields:
            columns = [getattr(schema, field) for field in query.join_fields]
            for col in columns:
                cursor = cursor.options(joinedload(col))
        
        if query.filter_by:
            cursor = cursor.where(text(query.filter_by))
        
        if query.order_by:
            cursor = cursor.order_by(text(query.order_by))

        if query.group_by:
            cursor = cursor.group_by(text(query.group_by))
            if query.having:
                cursor = cursor.having(text(query.having))

        
        cursor = cursor.limit(query.limit)
        cursor = cursor.offset(query.skip)

        return cursor.all()

    async def createOne(self, data: BaseModel, schema: DeclarativeBase):
        model = schema(**data.model_dump())
        self.session.add(model)
        self.session.commit()
        return model

    async def updateOne(self, id: str, data: BaseModel, schema: DeclarativeBase):
        model = self.getOne(id, schema)
        if not model: 
            raise exc.NoResultFound()

        for key, value in data.model_dump().items():
            setattr(model, key, value)
        
        self.session.commit()
        return model

    async def deleteOne(self, id: str, schema: DeclarativeBase):
        model = self.getOne(id, schema)
        if not model:
            raise exc.NoResultFound()
        
        self.session.delete(model)
