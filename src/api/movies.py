"""Endpoints relacionados con peliculas."""

from __future__ import annotations
from flask import Blueprint, jsonify, request
from src.extensions import db
from src.models import Movie

bp = Blueprint("movies", __name__, url_prefix="/movies")


class MovieService:
    """Orquesta la logica de negocio para el recurso Movie."""

    def list_movies(self) -> list[dict]:
        """Retorna todas las peliculas registradas."""
        movies = Movie.query.all()
        return [m.to_dict() for m in movies]

    def create_movie(self, payload: dict) -> dict:
        """Crea una nueva pelicula."""
        if not payload.get("title"):
            raise ValueError("El campo 'title' es obligatorio")

        movie = Movie(
            title=payload["title"],
            genre=payload.get("genre"),
            release_year=payload.get("release_year"),
        )
        db.session.add(movie)
        db.session.commit()
        return movie.to_dict()

    def get_movie(self, movie_id: int) -> dict:
        """Obtiene una pelicula por su identificador."""
        movie = Movie.query.get(movie_id)
        if not movie:
            raise LookupError("Película no encontrada")
        return movie.to_dict()

    def update_movie(self, movie_id: int, payload: dict) -> dict:
        """Actualiza los datos de una pelicula."""
        movie = Movie.query.get(movie_id)
        if not movie:
            raise LookupError("Película no encontrada")

        movie.title = payload.get("title", movie.title)
        movie.genre = payload.get("genre", movie.genre)
        movie.release_year = payload.get("release_year", movie.release_year)
        db.session.commit()
        return movie.to_dict()

    def delete_movie(self, movie_id: int) -> None:
        """Elimina una pelicula existente."""
        movie = Movie.query.get(movie_id)
        if not movie:
            raise LookupError("Película no encontrada")
        db.session.delete(movie)
        db.session.commit()


service = MovieService()


@bp.get("/")
def list_movies():
    try:
        movies = service.list_movies()
        return jsonify(movies), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.post("/")
def create_movie():
    payload = request.get_json(silent=True) or {}
    try:
        movie = service.create_movie(payload)
        return jsonify(movie), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp.get("/<int:movie_id>")
def retrieve_movie(movie_id: int):
    try:
        movie = service.get_movie(movie_id)
        return jsonify(movie), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


@bp.put("/<int:movie_id>")
def update_movie(movie_id: int):
    payload = request.get_json(silent=True) or {}
    try:
        movie = service.update_movie(movie_id, payload)
        return jsonify(movie), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


@bp.delete("/<int:movie_id>")
def delete_movie(movie_id: int):
    try:
        service.delete_movie(movie_id)
        return "", 204
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
