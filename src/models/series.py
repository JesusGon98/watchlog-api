"""Modelo para series disponibles en el catalogo."""

from __future__ import annotations

from datetime import datetime

from src.extensions import db


class Series(db.Model):
    """Representa una serie cargada por los usuarios."""

    __tablename__ = "series"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    synopsis = db.Column(db.Text)
    genres = db.Column(db.String(100))
    image_url = db.Column(db.String(250))
    total_seasons = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacion con Season (one-to-many)
    seasons = db.relationship("Season", back_populates="series", lazy=True)
    # Relacion con WatchEntry
    watch_entries = db.relationship("WatchEntry", back_populates="series", lazy=True)

    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        return f"<Series id={self.id} title={self.title}>"

    def to_dict(self, include_seasons: bool = False) -> dict:
        """Serializa la serie y opcionalmente sus temporadas."""
        # TODO: reemplazar por serializacion real usando marshmallow o similar.
        data = {
            "id": self.id,
            "title": self.title,
            "synopsis": self.synopsis,
            "genres": self.genres,
            "image_url": self.image_url,
            "total_seasons": self.total_seasons,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if include_seasons:
            data["seasons"] = [s.to_dict() for s in self.seasons]
        return data
