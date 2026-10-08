import os

from application import create_app
from config import ProductionConfig


if os.getenv("FLASK_ENV") == "production":
    app = create_app(ProductionConfig)
else:
    app = create_app()


if __name__ == "__main__":
    app.run()