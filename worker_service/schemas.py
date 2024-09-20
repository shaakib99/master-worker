from database_service.mysql_service import MySQLService
from sqlalchemy import Column, Integer, Boolean, String, DateTime
from datetime import datetime, timezone

Base = MySQLService.get_base()

class WorkerSchema(Base):
    __tablename__ = 'workers'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    unique_id = Column(String(255), nullable=False)
    host_ip = Column(String(255), nullable=False)
    status = Column(String(8), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

class PortsSchema(Base):
    __tablename__ = 'ports'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    worker_id = Column(Integer)
    port = Column(Integer)
    mapped_port = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

class EnvironmentVariablesSchema(Base):
    __tablename__ = 'environment_variables'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    worker_id = Column(Integer)
    name = Column(Integer)
    value = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))