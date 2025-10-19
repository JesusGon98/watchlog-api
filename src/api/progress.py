"""Endpoints para controlar el progreso de los usuarios."""

from __future__ import annotations
from flask import Blueprint, jsonify, request
from src.extensions import db
from src.models import User, Movie, Series, WatchEntry

bp = Blueprint("progress", __name__, url_prefix="/")


class ProgressService:
    """Coordina operaciones sobre la lista de seguimiento y progreso."""

    def list_watchlist(self, user_id: int) -> list[dict]:
        entries = WatchEntry.query.filter_by(user_id=user_id).all()
        return [e.to_dict() for e in entries]

    def add_movie(self, user_id: int, movie_id: int) -> dict:
        user = User.query.get(user_id)
        movie = Movie.query.get(movie_id)
        if not user or not movie:
            raise LookupError("Usuario o película no encontrados")

        entry = WatchEntry(user_id=user_id, movie_id=movie_id, total_episodes=1)
        db.session.add(entry)
        db.session.commit()
        return entry.to_dict()

    def add_series(self, user_id: int, series_id: int) -> dict:
        user = User.query.get(user_id)
        series = Series.query.get(series_id)
        if not user or not series:
            raise LookupError("Usuario o serie no encontrados")

        entry = WatchEntry(
            user_id=user_id,
            series_id=series_id,
            total_episodes=0,
            watched_episodes=0,
        )
        db.session.add(entry)
        db.session.commit()
        return entry.to_dict()

    def update_series_progress(self, user_id: int, series_id: int, payload: dict) -> dict:
        entry = WatchEntry.query.filter_by(user_id=user_id, series_id=series_id).first()
        if not entry:
            raise LookupError("Registro no encontrado")

        entry.watched_episodes = min(
            payload.get("watched_episodes", entry.watched_episodes),
            entry.total_episodes or payload.get("total_episodes", 0),
        )
        entry.total_episodes = payload.get("total_episodes", entry.total_episodes)
        entry.status = payload.get("status", entry.status)
        db.session.commit()
        return entry.to_dict()


service = ProgressService()


@bp.get("/me/watchlist")
def get_my_watchlist():
    user_id = request.headers.get("X-User-Id", type=int)
    if not user_id:
        return jsonify({"error": "Falta el header X-User-Id"}), 400
    try:
        data = service.list_watchlist(user_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.post("/watchlist/movies/<int:movie_id>")
def add_movie_to_watchlist(movie_id: int):
    user_id = request.headers.get("X-User-Id", type=int)
    if not user_id:
        return jsonify({"error": "Falta el header X-User-Id"}), 400
    try:
        entry = service.add_movie(user_id, movie_id)
        return jsonify(entry), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.post("/watchlist/series/<int:series_id>")
def add_series_to_watchlist(series_id: int):
    user_id = request.headers.get("X-User-Id", type=int)
    if not user_id:
        return jsonify({"error": "Falta el header X-User-Id"}), 400
    try:
        entry = service.add_series(user_id, series_id)
        return jsonify(entry), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.patch("/progress/series/<int:series_id>")
def update_series_progress(series_id: int):
    user_id = request.headers.get("X-User-Id", type=int)
    if not user_id:
        return jsonify({"error": "Falta el header X-User-Id"}), 400
    payload = request.get_json(silent=True) or {}
    try:
        entry = service.update_series_progress(user_id, series_id, payload)
        return jsonify(entry), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
