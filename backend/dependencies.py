"""
### Dependencies Injection dùng tương tự như middleware

Các dependencies không được gọi trực tiếp, mà phải được sử dụng trong route argument hoặc trong dependencies khác
- Các `route dependecy` là CamelCase, được phép gọi tại route và trong các dependency khác 
- Các `nested dependencies` là snake_case, chỉ được phép gọi trong dependecy
"""

from fastapi import Depends, Cookie, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from db import engine, ClientUtils
from typing import Annotated, TypedDict
from errors import *


def GetSession():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def GetClientUtils():
    session = Session(engine)
    try:
        yield ClientUtils(session)
    finally:
        session.close()


def GetClientCookie(client_id: Annotated[str | None, Cookie(alias='client-id')] = None):
    return client_id


def auth_flow(client_id: str, client_utils: Annotated[ClientUtils, Depends(GetClientUtils)]):
    """
    Return `Client` or exceptions

    - `HeaderMissing`
    - `ClientNotFound`
    - `ClientTimeOut`
    """
    client_in_db = client_utils.find_client(client_id)
    client_utils.verify_client(client_in_db)
    return client_in_db


def LoginOptional(client_id: Annotated[str | None, Depends(GetClientCookie)],
                  client_utils: Annotated[ClientUtils, Depends(GetClientUtils)]):
    try:
        if client_id is None:
            raise HeaderMissing
        client = auth_flow(client_id, client_utils)
        return client
    except ClientTimeOut as e:
        client_in_db = e.client_in_db
        new_client_id = str(uuid4())
        client_utils.update_refresh_token(client_in_db, new_client_id)
        return client_in_db

    except (ClientNotFound, HeaderMissing) as e:
        new_client_id = str(uuid4())
        new_client = client_utils.create_client(new_client_id)
        return new_client


def LoginRequired(client_id: Annotated[str | None, Depends(GetClientCookie)],
                  client_utils: Annotated[ClientUtils, Depends(GetClientUtils)]):
    try:
        client = auth_flow(client_id, client_utils)
        return client

    except ClientTimeOut as e:
        client_in_db = e.client_in_db
        new_client_id = str(uuid4())
        client_utils.update_refresh_token(client_in_db, new_client_id)
        return client_in_db

    except (HeaderMissing, ClientNotFound) as e:
        raise HTTPException(400, 'Client ID invalid')


class PaginationInterface(TypedDict):
    page: int
    limit: int


async def Pagination(page: int = 1, limit: int = 5) -> PaginationInterface:
    return {"page": page, "limit": limit}
