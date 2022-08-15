SQLALCHEMY_SQLITE_DATABASE_URL = "sqlite:///./dictionary_api.db"
INITIAL_DICTIONARY_FILE = 'initial_dictionary.txt'

STATISTICS_DICT_FORMAT = {
    "averageRequestHandleTimeMs": None,
    "requestHandledCount": None,
    "wordCount": None
}

PATH_DICT = ['/dictionary', '/statistics', '/update_dictionary', '/get_action_status']
