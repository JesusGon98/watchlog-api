"""Modelo para usuarios que usan la plataforma."""

from __future__ import annotations
from datetime import datetime
from src.extensions import db


class User(db.Model):
    """Representa a un usuario (simulado mediante el header X-User-Id)."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # 👈 Clave primaria activa
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacion con WatchEntry (one-to-many)
    watch_entries = db.relationship("WatchEntry", back_populates="user", lazy=True)

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
        }
