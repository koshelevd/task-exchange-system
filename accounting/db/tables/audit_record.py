from db.tables.base import BaseModel
from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.orm import relationship


class AuditRecord(BaseModel):
    """Audit record model."""

    __tablename__ = "audit_log"

    sum = Column(BigInteger, nullable=False, comment="Sum")

    account_id = Column(BigInteger, ForeignKey("account.id"), nullable=False, comment="Account id")
    account = relationship("Account", back_populates="audit_records", lazy="noload")

    task_id = Column(BigInteger, ForeignKey("task.id"), nullable=False, comment="Task id")
    task = relationship("Task", back_populates="audit_records", lazy="noload")
