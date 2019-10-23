from typing import Optional

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.db_models.dataset import Label, DBFile
from app.db.helpers import get_or_create


def create_label(db_session: Session, *, label: str):
    label_obj = get_label(db_session, label=label)
    if not label_obj:
        label_obj = Label(
            label=label
        )
        db_session.add(label_obj)
        db_session.commit()
        db_session.refresh(label_obj)
        return True, label_obj
    return False, label_obj


def get_all_labels(db_session: Session):
    return db_session.query(Label).all()


def get_label(db_session: Session, label: Optional[str] = None, label_id: Optional[int] = None):
    if label_id:
        return db_session.query(Label).get(label_id)
    if label:
        return db_session.query(Label).filter(Label.label == label).first()

    return None


def get_file(db_session: Session, file_id: int):
    return db_session.query(DBFile).get(file_id)


def upload_dataset_entry(db_session: Session, *, dbfile: UploadFile, label: Label):
    return get_or_create(db_session, DBFile, data=dbfile.file.read(), label=label)


def update_label(db_session: Session, label_id: int, new_name: str):
    label = get_label(db_session=db_session, label_id=label_id)
    if label:
        label.label = new_name
        db_session.commit()
        return label
    return None
