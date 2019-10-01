import librosa
import tempfile
import numpy as np
import requests
import json
from os import path
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.api.utils.db import get_db
from db_models.dbfile import DBFile
from db_models.inference import LabelsEnum

router = APIRouter()


async def get_single_inference(content):
    data = json.dumps({"signature_name": "serving_default", "instances": content.tolist()})

    json_response = requests.post("http://localhost:8501/v1/models/urbanSound/versions/1:predict", data=data,
                                  headers={"content-type": "application/json"})
    return json_response.json()['predictions']


async def _process_image(content: bytes, db: Session, save_file: bool = True):
    inference = await get_single_inference(content)
    if save_file:
        await _save_file(content, db)

    return inference


async def get_features(filename):
    y, sr = librosa.load(filename)
    mfccs = np.mean(librosa.feature.mfcc(y, sr, n_mfcc=40).T, axis=0)
    melspectrogram = np.mean(librosa.feature.melspectrogram(y=y, sr=sr, n_mels=40, fmax=8000).T, axis=0)
    chroma_stft = np.mean(librosa.feature.chroma_stft(y=y, sr=sr, n_chroma=40).T, axis=0)
    chroma_cq = np.mean(librosa.feature.chroma_cqt(y=y, sr=sr, n_chroma=40).T, axis=0)
    chroma_cens = np.mean(librosa.feature.chroma_cens(y=y, sr=sr, n_chroma=40).T, axis=0)
    return np.reshape(np.vstack((mfccs, melspectrogram, chroma_stft, chroma_cq, chroma_cens)), (1, 40, 5))


async def _save_file(content, db: Session):
    newfile = DBFile(data=content)
    db.add(newfile)
    db.commit()


@router.post("/upload")
async def upload_file(*, db: Session = Depends(get_db), file: UploadFile = File(...)):
    print(file.content_type)
    ctype = file.content_type
    try:
        if ctype == "audio/wav":
            with tempfile.NamedTemporaryFile(suffix=".wav", prefix=path.basename(__file__)) as tmp:
                b = await file.read()
                tmp.write(b)
                return [{LabelsEnum(i).name: float("{0:.2f}".format(val)) for i, val in enumerate(result)} for result in
                        await get_single_inference(await get_features(path.join(tempfile.gettempdir(), str(tmp.name))))]

            # save_image(process_audio(await file.read()))
        else:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Only wav and jpeg supported")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process file")
