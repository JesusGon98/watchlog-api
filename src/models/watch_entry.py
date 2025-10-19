"""Modelo puente que guarda el progreso del usuario."""

from __future__ import annotations

from datetime import datetime

from src.extensions import db


class WatchEntry(db.Model):
    """Relacion entre un usuario y un contenido (pelicula o serie)."""

    __tablename__ = "watch_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=True)
    status = db.Column(db.String(20), default="in_progress")
    current_season = db.Column(db.Integer, default=0)
    current_episode = db.Column(db.Integer, default=0)
    watched_episodes = db.Column(db.Integer, default=0)
    total_episodes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    user = db.relationship("User", back_populates="watch_entries")
    movie = db.relationship("Movie", back_populates="watch_entries")
    series = db.relationship("Series", back_populates="watch_entries")

    def percentage_watched(self) -> float:
        """Calcula el porcentaje completado para el contenido asociado."""
        if not self.total_episodes:
            return 0.0
        percentage = (self.watched_episodes / self.total_episodes) * 100
        return min(percentage, 100.0)

    def mark_as_watched(self) -> None:
        """Marca el contenido como completado."""
        self.status = "completed"
        self.watched_episodes = self.total_episodes
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def to_dict(self) -> dict:
        """Serializa la entrada para respuestas JSON."""
        # TODO: reemplazar con serializacion acorde al modelo final.
        return {
              "id": self.id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "series_id": self.series_id,
            "status": self.status,
            "current_season": self.current_season,
            "current_episode": self.current_episode,
            "watched_episodes": self.watched_episodes,
            "total_episodes": self.total_episodes,
            "percentage_watched": self.percentage_watched(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
