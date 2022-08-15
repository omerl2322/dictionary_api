from sqlite3 import DatabaseError

from database import get_db
from models import Words, Actions
from orm_handler.words import bulk_insert_words


def upload_file_to_db(txt_file, request_id):
    """
    uploading file content to the db and associating it with a request id
    :param txt_file: file as UploadFile
    :param request_id: uuid as str
    :return: None
    """
    db = next(get_db())
    # insert new action
    upsert_action_status(request_id)
    # convert content from bytes to str
    new_words_list_bytes = txt_file.file.read().splitlines()
    new_words_list = list(map(lambda x: x.decode(), new_words_list_bytes))
    # get common values
    common_words_list = db.query(Words).filter(Words.word.in_(new_words_list)).all()
    common_words_str_list = list(map(lambda x: x.word, common_words_list))
    # if common words list is empty get the new words list, otherwise subtract common values
    values_to_update_list = new_words_list if not common_words_list else [item for item in new_words_list if
                                                                          item not in common_words_str_list]
    try:
        bulk_insert_words(values_to_update_list)
        # update request status
        upsert_action_status(request_id, status='success')
    except DatabaseError as err:
        failed_message = f'failed with error: {err}'
        upsert_action_status(request_id, status=failed_message)


def upsert_action_status(request_id, status='in progress'):
    """
    update or insert a record into the api_actions table
    :param request_id: uuid as str
    :param status: str
    :return: None
    """
    db = next(get_db())
    action = db.query(Actions).filter(Actions.request_id == request_id).first()
    if action is None:
        # means it is a new action
        new_action = Actions(action='upload_file', request_id=request_id, status=status)
        db.add(new_action)
    else:
        # this action exists
        action.status = status
        db.add(action)
    db.commit()
