from fastapi import Request, HTTPException
from db import ClientUtils, Client, engine
from sqlalchemy.orm import Session
from errors import *
from uuid import uuid4


session = Session(engine)
client_utils = ClientUtils(session)

def get_client_id(request: Request):
    client_header = request.headers.get('client-id')
    if client_header is None:
        raise HeaderMissing
    return client_header


class Request:
    def __init__(self, client_id) -> None:
        self.headers = {'client-id': client_id}

def AuthFlow(request:Request, client_utils: ClientUtils):
    """
    Return `Client` or exceptions

    - `HeaderMissing`
    - `ClientNotFound`
    - `ClientTimeOut`
    """
    client_id = get_client_id(request)
    client_in_db = client_utils.find_client(client_id)
    client_utils.verify_client(client_in_db)
    return client_in_db
    

def LoginRequired(request:Request, client_utils: ClientUtils) -> Client:
    try:
        client = AuthFlow(request, client_utils)
        return client
    
    except ClientTimeOut as e:
        client_in_db = e.client_in_db
        new_client_id = str(uuid4())
        client_utils.update_refresh_token(client_in_db, new_client_id)
        return client_in_db
    
    except (HeaderMissing, ClientNotFound) as e:
        raise HTTPException(400, 'Client ID invalid')
    

def LoginOptional(request:Request, client_utils: ClientUtils) -> Client:
    try:
        client = AuthFlow(request, client_utils)
        return client
    
    except ClientTimeOut as e:
        client_in_db = e.client_in_db
        new_client_id = str(uuid4())
        client_utils.update_refresh_token(client_in_db, new_client_id)
        return client_in_db
    
    except (HeaderMissing, ClientNotFound) as e:
        new_client_id = str(uuid4())
        new_client = client_utils.create_client(new_client_id)
        return new_client




# request = Request('hello-world')

# LoginRequired(request, client_utils)