import os

from app import crud
from app.models.user import UserCreate


def init_db(db_session):
    FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER", default="admin")
    FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD", default="admin")

    user = crud.user.get_by_email(db_session, email=FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=FIRST_SUPERUSER,
            password=FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db_session, user_in=user_in)

    start_labels = ("children_playing", "air_conditioner", "car_horn", "dog_bark",
                    "drilling", "engine_idling", "gun_shot", "jackhammer", "siren", "street_music")

    for label in start_labels:
        crud.dataset.create_label(db_session, label=label)
