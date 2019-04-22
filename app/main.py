from routes import get_app
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('api.log'))
logger.setLevel(logging.INFO)

app = get_app()
