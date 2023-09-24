from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import event, and_, Integer, String
from utils import ensure_path_exist
from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

class Room(db.Model):
    """
    @ Parameters

    - name: str
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)


class Dataframe(db.Model):
    __table_args__ = (
        db.UniqueConstraint('file_name', 'room_name'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    room_name: Mapped[str] = mapped_column(String, nullable=False)
    alias: Mapped[Optional[str]]


@event.listens_for(Room, "after_insert")
def ensure_path(mapper, connection, target: Room):
    ensure_path_exist(f'./uploads/{target.name}')


class UserUtils:
    """
    Utilities functions for `User` table, to reduce import in controller file
    """
    @staticmethod
    def find_user(username):
        return User.query.filter(User.username == username).one_or_none()
    
    @staticmethod
    def create_user(username, password):
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()


class RoomUtils:
    """
    Utilities functions for `Room` table, to reduce import in controller file
    """
    @staticmethod
    def add_new_room(name: str):
        new_room = Room(name=name)
        db.session.add(new_room)
        db.session.commit()

    @staticmethod
    def find_room(name: str):
        return Room.query.filter(Room.name == name).one_or_none()

    @staticmethod
    def delete_room(name: str):
        obj = Room.query.filter(Room.name == name).one_or_none()
        if obj is not None:
            db.session.delete(obj)
            db.session.commit()


class DataframeUtils:
    """
    Utilities functions for `DataframeNameUtils` table, to reduce import in controller file
    """
    @staticmethod
    def add_dataframe(room_name: str, file_name: str, alias: Optional[str] = None):
        if alias is not None:
            new_df = Dataframe(room_name=room_name,
                               file_name=file_name, alias=alias)
        else:
            new_df = Dataframe(room_name=room_name, file_name=file_name)
        db.session.add(new_df)
        db.session.commit()

    @staticmethod
    def list_dataframe_from_room(room_name) -> List[Dataframe]:
        return Dataframe.query.filter(Dataframe.room_name == room_name).all()

    @staticmethod
    def get_alias(room_name, file_name):
        result: Dataframe = Dataframe.query.filter(and_(
            Dataframe.room_name == room_name, Dataframe.file_name == file_name)).one_or_none()
        if result is not None:
            return result.alias
        else:
            return result

    @staticmethod
    def update_alias(room_name, file_name, new_alias):
        obj:Dataframe = Dataframe.query.filter(
            and_(Dataframe.room_name == room_name, Dataframe.file_name == file_name)).first()
        obj.alias = new_alias
        db.session.commit()