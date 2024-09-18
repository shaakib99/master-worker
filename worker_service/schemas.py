from database_service.mysql_service import MySQLService
from sqlalchemy import Column, Integer

Base = MySQLService.get_base()

class WorkerSchema(Base):
    __tablename__ = 'workers'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)