from sqlalchemy import exc, func

from database import get_db, row_handler
from models import Requests


def create_request(request_handle_time):
    """
    Create request on api_requests table
    :param request_handle_time: in millisecond
    :return: None
    """
    db = next(get_db())
    request = Requests(request_handle_time=request_handle_time)
    try:
        db.add(request)
        db.commit()
    except exc.SQLAlchemyError as e:
        print(f'there was an error with create_request method: {e}')


def get_requests_amount():
    """
    get the amount of requests
    :return: requests amount
    """
    db = next(get_db())
    requests_amount = db.query(func.max(Requests.request_number)).first()
    return row_handler(requests_amount)


def calculate_average_request_handle_time():
    """
    calculation of average processing of requests
    :return: average as float
    """
    db = next(get_db())
    average_request_handle = db.query(func.avg(Requests.request_handle_time)).first()
    return row_handler(average_request_handle)
