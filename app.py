from flask import Flask
from src.extensions import db, migrate
from src.config import Config
from src.api.health import health_bp
from src.api.movies import movies_bp
from src.api.series import series_bp
from src.api.progress import progress_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(series_bp)
    app.register_blueprint(progress_bp)

    return app

app = create_app()

