"""Modelo principal para las peliculas."""

from __future__ import annotations

from datetime import datetime

from src.extensions import db


class Movie(db.Model):
    """Representa una pelicula dentro del catalogo."""

    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(50))
    release_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacion con WatchEntry (one-to-many)
    watch_entries = db.relationship("WatchEntry", back_populates="movie", lazy=True)

    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        # TODO: ajustar los campos utilizados en la representacion.
        return f"<Movie id={self.id} title={self.title}>"

    def to_dict(self) -> dict:
        """Serializa la instancia para respuestas JSON."""
        # TODO: reemplazar esta implementacion temporal por serializacion real.
        return {
           "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "release_year": self.release_year,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
