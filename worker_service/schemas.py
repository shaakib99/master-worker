from database_service.mysql_service import MySQLService
from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = MySQLService.get_base()

class WorkerSchema(Base):
    __tablename__ = 'workers'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    unique_id = Column(String(255), nullable=False)
    image_name = Column(String(255), nullable=False)
    host_ip = Column(String(255), nullable=False)
    status = Column(String(8), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

class PortsSchema(Base):
    __tablename__ = 'ports'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id', ondelete='CASCADE'))
    port = Column(Integer)
    mapped_port = Column(Integer)
    should_add_to_load_balancer = Column(Boolean, default=False)
    update_prometheus_config = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    worker = relationship("WorkerSchema")

class EnvironmentVariablesSchema(Base):
    __tablename__ = 'environment_variables'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id', ondelete='CASCADE'))
    name = Column(String(255))
    value = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))