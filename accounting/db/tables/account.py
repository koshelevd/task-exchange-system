from db.tables.base import BaseModel
from sqlalchemy import BigInteger, Column, Date, Float, ForeignKey
from sqlalchemy.orm import relationship


class Account(BaseModel):
    """Account model."""

    __tablename__ = "account"

    balance = Column(Float, nullable=False, comment="Payment")
    date = Column(Date, nullable=False, comment="Date")

    employee_id = Column(BigInteger, ForeignKey("employee.id"), nullable=False, comment="Employee id")
    employee = relationship("Employee", back_populates="accounts", lazy="noload")

    audit_records = relationship("AuditRecord", back_populates="account", lazy="noload")
