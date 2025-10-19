"""Modelo que representa una temporada de una serie."""

from __future__ import annotations

from src.extensions import db


class Season(db.Model):
    """Temporada asociada a una serie."""

    __tablename__ = "seasons"

    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    episodes_count = db.Column(db.Integer, default=0)

    # restriccion unica por (series_id, number)
    __table_args__ = (db.UniqueConstraint("series_id", "number", name="unique_series_season"),)

    # Relacion back_populates con Series
    series = db.relationship("Series", back_populates="seasons")


    def to_dict(self) -> dict:
        """Serializa la temporada en un diccionario."""
        # TODO: reemplazar esta implementacion por la serializacion real.
        return {
             "id": self.id,
            "series_id": self.series_id,
            "number": self.number,
            "episodes_count": self.episodes_count,
        }
