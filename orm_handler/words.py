from sqlite3 import DatabaseError

from sqlalchemy import func, exc

from constants import INITIAL_DICTIONARY_FILE
from database import get_db, row_handler
from models import Words


def bulk_insert_words(words, init=True):
    """
    Inserting a list of words into the db
    :param words: list of words as str
    :param init: bool flag, used for inserting bulk at startup
    :return: None
    """
    db = next(get_db())
    obj_list = list(map(lambda x: Words(word=x), words))
    try:
        db.bulk_save_objects(obj_list)
        db.commit()
    except exc.SQLAlchemyError as e:
        print(f'there was an error with bulk_insert_words method: {e}')
        if init:
            raise DatabaseError(f'there was an error with bulk_insert_words method: {e}')


def init_dictionary():
    """
    inserting an initial dictionary - running on startup
    :return: None
    """
    with open(INITIAL_DICTIONARY_FILE) as f:
        words = f.read().splitlines()
    bulk_insert_words(words, init=False)


# init_dictionary()


def get_words_counter():
    """
    Count how many words there are in db
    :return: counter
    """
    db = next(get_db())
    words_counter = db.query(func.count(Words.word)).first()
    return row_handler(words_counter)


def words_by_prefix(prefix):
    """
    search for words by their prefix
    :param prefix: a combination of several letters, for example: "AAB"
    :return: if found in the dictionary - A list of matching words
    """
    db = next(get_db())
    like_statement = "{}%".format(prefix)
    prefix_words = db.query(Words).filter(Words.word.like(like_statement)).all()
    if not prefix_words:
        return []
    return [item.word for item in prefix_words]
