from typing import Optional
from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import create_engine, select, update
from datetime import datetime
from errors import *
from uuid import uuid4
from time import sleep
engine = create_engine("sqlite:///sessions.db")


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = 'client'
    id: Mapped[int] = mapped_column(primary_key=True)
    server_cookie: Mapped[str] = mapped_column(
        String, unique=True, nullable=False)
    client_cookie: Mapped[str] = mapped_column(
        String, unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now())
    lastest_checkin: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now())
    total_consume: Mapped[int] = mapped_column(BigInteger, default=0)


CLIENT_AGE_HOUR = 8


class ClientUtils:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_client(self, client_id: str) -> Client:
        server_cookie = str(uuid4())
        new_client = Client(server_cookie=server_cookie,
                            client_cookie=client_id)
        self.session.add(new_client)
        self.session.commit()
        return new_client

    def find_client(self, client_id: str) -> Client:
        statement = select(Client).where(Client.client_cookie == client_id)
        client = self.session.scalar(statement)
        if client is None:
            raise ClientNotFound()
        return client

    def verify_client(self, client: Client):
        """
        Verify the user base on user id and age. If age is valid, register new `latest_checkin`

        @Raise UserWarning subclass:

        - `ClientNotFound`: client_id does not match db records
        - `ClientTimeOut`: client age timeout
        """
        now = datetime.now()
        def hour_diff(x, y): return round((x-y).total_seconds() / 3600, 0)
        if hour_diff(now, client.lastest_checkin) > CLIENT_AGE_HOUR:
            raise ClientTimeOut(client)
        else:
            client.lastest_checkin = now
            self.session.commit()

    def update_refresh_token(self, client:Client, new_client_id:str):
        now = datetime.now()
        client.client_cookie = new_client_id
        client.lastest_checkin = now
        self.session.commit()
        return client


Base.metadata.create_all(engine)

if __name__ == '__main__':
    with Session(engine) as session:
        client_utils = ClientUtils(session)
        dt = datetime(2023, 9, 29)
        client_cookie = 'hello-world'
        server_cookie = str(uuid4())
        new_client = Client(server_cookie=server_cookie, client_cookie=client_cookie, lastest_checkin=dt, created_at=dt)
        session.add(new_client)
        session.commit()
        # new_client = ClientUtils.find_client('ajsfhgjasgfjhasg', session)
        # sleep(5)
        # ClientUtils.verify_client(new_client, session)
