from sqlalchemy import BigInteger, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db.tables.base import BaseModel


class Role(BaseModel):
    """Role model."""

    __tablename__ = "roles"

    name = Column(String(255), nullable=False, comment="Name")

    users = relationship("User", back_populates="role", lazy="noload")

    __table_args__ = (
        UniqueConstraint(
            "name",
        ),
    )

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"


class User(BaseModel):
    """User model."""

    __tablename__ = "users"

    email = Column(String(255), nullable=False, comment="Email")
    password = Column(String(255), nullable=False, comment="Password")

    role_id = Column(BigInteger, ForeignKey("roles.id"), nullable=False, comment="Role id")
    role = relationship("Role", back_populates="users", lazy="noload")

    __table_args__ = (
        UniqueConstraint(
            "email",
        ),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
