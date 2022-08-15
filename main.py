import uuid
import time
import uvicorn
from sqlalchemy.orm import Session

from models import Actions
from database import get_db
from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks, Depends, Request

from constants import STATISTICS_DICT_FORMAT, PATH_DICT
from orm_handler.actions import upload_file_to_db
from orm_handler.requests import calculate_average_request_handle_time, get_requests_amount, create_request
from orm_handler.words import get_words_counter, words_by_prefix

app = FastAPI(title='Dictionary API',
              description='As part of an exercise')


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    # convert seconds to milliseconds
    process_time = (time.time() - start_time) * 1000
    if request.url.path in PATH_DICT:
        create_request(process_time)
    return response


@app.get('/dictionary')
def get_words_by_prefix(prefix: str):
    if prefix.isnumeric():
        raise HTTPException(400, detail="invalid input. Please enter letters")
    return words_by_prefix(prefix)


@app.get('/statistics')
def get_statistics():
    response_template = STATISTICS_DICT_FORMAT
    response_template['averageRequestHandleTimeMs'] = calculate_average_request_handle_time()
    response_template['requestHandledCount'] = get_requests_amount()
    response_template['wordCount'] = get_words_counter()
    return response_template


@app.post('/update_dictionary')
async def update_dictionary(background_tasks: BackgroundTasks, txt_file: UploadFile = File(...)):
    # check file extension
    if txt_file.content_type != "text/plain":
        raise HTTPException(400, detail="invalid document type. The file should be in txt format")
    # generate request_id
    request_id = str(uuid.uuid4())
    # update_dictionary in db - as background task
    background_tasks.add_task(upload_file_to_db, txt_file, request_id)
    return {"message": "the file has been received. request status can be tracked with get_action_status method",
            "request_id": request_id}


@app.get('/get_action_status')
def get_action_status(request_id: str, db: Session = Depends(get_db)):
    if len(request_id) != 36:
        raise HTTPException(400, detail="invalid request_id guid")
    action = db.query(Actions).filter(Actions.request_id == request_id).first()
    if action is None:
        raise HTTPException(404, detail=f"request_id: {request_id} does not exist")
    return {"request_id": request_id, "status": action.status}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
