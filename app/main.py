from routes import get_app
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('api.log'))
logger.setLevel(logging.INFO)

app = get_app()

print("HOLA")

from gunicorn.app.base import Application
if __name__ == "__main__":
    Application().run(app)