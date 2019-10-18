# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.db_models.kit import Kit # noga
from app.db_models.dbfile import DBFile # noga
from app.db_models.inference import Inference, Labels  # noga