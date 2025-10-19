"""Endpoints relacionados con series y temporadas."""

from __future__ import annotations
from flask import Blueprint, jsonify, request
from src.extensions import db
from src.models import Series, Season

bp = Blueprint("series", __name__, url_prefix="/series")


class SeriesService:
    """Gestiona las operaciones CRUD sobre Series y Seasons."""

    def list_series(self) -> list[dict]:
        series = Series.query.all()
        return [s.to_dict(include_seasons=True) for s in series]

    def create_series(self, payload: dict) -> dict:
        if not payload.get("title"):
            raise ValueError("El campo 'title' es obligatorio")
        series = Series(
            title=payload["title"],
            synopsis=payload.get("synopsis"),
            genres=payload.get("genres"),
            total_seasons=payload.get("total_seasons", 0),
        )
        db.session.add(series)
        db.session.commit()
        return series.to_dict()

    def get_series(self, series_id: int) -> dict:
        series = Series.query.get(series_id)
        if not series:
            raise LookupError("Serie no encontrada")
        return series.to_dict(include_seasons=True)

    def update_series(self, series_id: int, payload: dict) -> dict:
        series = Series.query.get(series_id)
        if not series:
            raise LookupError("Serie no encontrada")

        series.title = payload.get("title", series.title)
        series.synopsis = payload.get("synopsis", series.synopsis)
        series.genres = payload.get("genres", series.genres)
        series.total_seasons = payload.get("total_seasons", series.total_seasons)
        db.session.commit()
        return series.to_dict(include_seasons=True)

    def delete_series(self, series_id: int) -> None:
        series = Series.query.get(series_id)
        if not series:
            raise LookupError("Serie no encontrada")
        db.session.delete(series)
        db.session.commit()

    def add_season(self, series_id: int, payload: dict) -> dict:
        series = Series.query.get(series_id)
        if not series:
            raise LookupError("Serie no encontrada")

        number = payload.get("number")
        episodes = payload.get("episodes_count", 0)
        if not number:
            raise ValueError("El campo 'number' es obligatorio")

        season = Season(series_id=series_id, number=number, episodes_count=episodes)
        db.session.add(season)
        db.session.commit()
        return season.to_dict()


service = SeriesService()


@bp.get("/")
def list_series():
    try:
        data = service.list_series()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.post("/")
def create_series():
    payload = request.get_json(silent=True) or {}
    try:
        series = service.create_series(payload)
        return jsonify(series), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.get("/<int:series_id>")
def retrieve_series(series_id: int):
    try:
        data = service.get_series(series_id)
        return jsonify(data), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


@bp.put("/<int:series_id>")
def update_series(series_id: int):
    payload = request.get_json(silent=True) or {}
    try:
        series = service.update_series(series_id, payload)
        return jsonify(series), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


@bp.delete("/<int:series_id>")
def delete_series(series_id: int):
    try:
        service.delete_series(series_id)
        return "", 204
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


@bp.post("/<int:series_id>/seasons")
def add_season(series_id: int):
    payload = request.get_json(silent=True) or {}
    try:
        season = service.add_season(series_id, payload)
        return jsonify(season), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
