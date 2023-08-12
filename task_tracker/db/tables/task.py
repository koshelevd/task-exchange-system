from enum import Enum

from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from db.tables.base import BaseModel


class Status(Enum):
    """Status enum."""

    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(BaseModel):
    """Task model."""

    __tablename__ = "task"

    description = Column(String(255), nullable=True, comment="Description")
    status = Column(ENUM(Status, schema="public"), nullable=False, comment="Status")
    fee = Column(BigInteger, nullable=False, comment="Fee")
    payment = Column(BigInteger, nullable=False, comment="Payment")

    employee_id = Column(BigInteger, ForeignKey("employee.id"), nullable=False, comment="Employee id")
    employee = relationship("Employee", back_populates="tasks", lazy="noload")

    def __repr__(self):
        return f"<Task(id={self.id}, description={self.description}, status={self.status}>"
