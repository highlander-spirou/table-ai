from typing import Union
from sqlalchemy.orm import Session
from db import Client, ClientUtils
from errors import *
from uuid import uuid4



class Request:
    def __init__(self) -> None:
        self.header = {'client-id': 'afsahkjasfhja'}

def get_client_id(request: Request):
    client_header = request.headers.get('client-id')
    if client_header is None:
        raise HeaderMissing
    return client_header


def AuthenticationFlow(request: Union[Request, str], session: Session) -> Client:
    """
    Provide authentication flow of request, and resolver that on Exception

    @ Params:
    - request: `Request` object of `str` of client-id
    """
    try:
        client_utils = ClientUtils(session)
        client_header = get_client_id(request)
        client_in_db = client_utils.find_client(client_header)
        client_utils.verify_client(client_in_db)
        return client_in_db

    except (HeaderMissing, ClientNotFound) as e:
        new_client_id = str(uuid4())
        new_client = client_utils.create_client(new_client_id)
        return new_client

    except ClientTimeOut as e:
        new_client_id = str(uuid4())
        client_utils.update_refresh_token(client_in_db, new_client_id)
        return client_in_db