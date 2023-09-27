from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import event, and_, Integer, String, ForeignKey
from utils import ensure_path_exist
from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from random import randint, seed


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_hash_str(s):
    seed(1)
    hashed = str(randint(1_000_000, 9_999_999_999))
    return s + '_' + hashed


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    rooms: Mapped[List['Room']] = relationship(back_populates="owner")


class Room(db.Model):
    """
    @ Parameters

    - name: str
    - owner: User
    """
    __table_args__ = (
        db.UniqueConstraint('owner_id', 'name'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_name: Mapped[Optional[str]] = mapped_column(
        String, nullable=False, unique=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="rooms")
    dataframes: Mapped[List['Dataframe']] = relationship(
        back_populates="room_owner")

    def get_dataframe_attr(self, attr: str):
        return [df.__getattribute__(attr) for df in self.dataframes]


class Dataframe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    alias: Mapped[Optional[str]]
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    room_owner: Mapped["Room"] = relationship(back_populates="dataframes")

    @property
    def short_name(self):
        return self.file_name.split('/')[1]
    
    @property
    def table_meta(self):
        return {'alias': self.alias, 'table_name': self.file_name}


@event.listens_for(Room, "before_insert")
def hash_room_name(mapper, connection, target: Room):
    target.hashed_name = create_hash_str(target.name)


@event.listens_for(Room, "after_insert")
def ensure_path(mapper, connection, target: Room):
    ensure_path_exist(f'./uploads/{target.hashed_name}')


class UserUtils:
    """
    Utilities functions for `User` table, to reduce import in controller file
    """
    @staticmethod
    def find_user(username):
        return User.query.filter(User.username == username).one_or_none()

    @staticmethod
    def create_user(username, password):
        new_user = User(username=username,
                        password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def login_user(username, password):
        user: User = User.query.filter(User.username == username).one_or_none()

        if user is not None and check_password_hash(user.password, password):
            return user
        else:
            raise Exception

    @staticmethod
    def list_room(user_id) -> List[Room]:
        user = User.query.filter(User.id == user_id).one_or_none()
        return user.rooms


class RoomUtils:
    """
    Utilities functions for `Room` table, to reduce import in controller file
    """
    @staticmethod
    def add_new_room(name: str, user: User) -> Room:
        new_room = Room(name=name, owner=user)
        db.session.add(new_room)
        db.session.commit()
        return new_room

    @staticmethod
    def find_room(name: str, current_user: User) -> Optional[Room]:
        return Room.query.filter(and_(Room.name == name, Room.owner_id == current_user.id)).one_or_none()

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
    def add_dataframe(room: Room, file_name: str):
        f = f'{room.hashed_name}/{file_name}'
        new_df = Dataframe(file_name=f, room_owner=room)
        db.session.add(new_df)
        db.session.commit()

    @staticmethod
    def update_alias(room_name, file_name, new_alias):
        obj: Dataframe = Dataframe.query.filter(
            and_(Dataframe.room_name == room_name, Dataframe.file_name == file_name)).first()
        obj.alias = new_alias
        db.session.commit()

    @staticmethod
    def verify_onwership(user_id: str, file_name: str):
        df:Dataframe = Dataframe.query.filter(Dataframe.file_name == file_name).one_or_none()
        return df.room_owner.owner_id  == user_id
    
    @staticmethod
    def find_dataframe(name) -> Dataframe:
        return Dataframe.query.filter(Dataframe.file_name == name).one()