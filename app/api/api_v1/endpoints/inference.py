from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.api.utils.db import get_db
from db_models.dbfile import DBFile
from PIL import Image

from db_models.inference import LabelsEnum
import io
import numpy
router = APIRouter()


async def get_inference(content):
    img = Image.open(io.BytesIO(content))
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()


    floating_model = input_details[0]['dtype'] == np.float32
    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    input_shape = input_details[0]['shape']
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)

    return {LabelsEnum(i): float(val) for i, val in enumerate(results)}

async def _process_image(content: bytes, db: Session, save_file: bool = True):
    inference = await get_inference(content)
    if save_file:
        await _save_file(content, db)

    return inference

async def _save_file(content, db: Session):
    newfile = DBFile(data=content)
    db.add(newfile)
    db.commit()


@router.post("/upload")
async def upload_file(*, db: Session = Depends(get_db), file: UploadFile = File(...)):
    print(file.content_type)
    ctype = file.content_type

    try:
        if ctype == "image/jpeg":
            await _process_image(await file.read(), db)
        # elif ctype is "audio/wav":
        #     save_image(process_audio(await file.read()))
        else:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Only wav and jpeg supported")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process file")
