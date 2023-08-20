from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from db.tables.base import BaseModel


class Employee(BaseModel):
    """Employee model."""

    __tablename__ = "employee"

    name = Column(String(255), nullable=True, comment="Name")
    role = Column(String(255), nullable=False, comment="Role")
    sso_id = Column(BigInteger, nullable=False, comment="SSO ID")

    accounts = relationship("Account", back_populates="employee", lazy="noload")

    def __repr__(self):
        return f"<Employee(id={self.id}, name={self.name}, role={self.role}, sso_id={self.sso_id})>"
