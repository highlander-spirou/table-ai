from pathlib import Path
from flask_wtf import FlaskForm
from wtforms.fields import StringField, MultipleFileField, SubmitField, PasswordField
from wtforms.validators import InputRequired, StopValidation, EqualTo
from models import RoomUtils, UserUtils

class MultiFileAllowed(object):
    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __get_file_ext(self, file_name):
        return Path(file_name).suffix

    def __call__(self, form, field):
        all_file_valid = all([self.__get_file_ext(
            i) in self.upload_set for i in field.data])
        if all_file_valid:
            return
        else:
            raise StopValidation('File type not match')


class CheckUsernameExisted(object):
    def __init__(self, message=None):
        self.message = message

    def __check_user_exist(self, username):
        return UserUtils.find_user(username) is not None

    def __call__(self, form, field):
        if self.__check_user_exist(field.data):
            raise StopValidation('Duplicated user name')
        else:
            return form

class CheckRoomIdExisted(object):
    def __init__(self, message=None):
        self.message = message

    def __check_room_exist(self, room_to_check):
        return RoomUtils.find_room(room_to_check) is not None

    def __call__(self, form, field):
        if self.__check_room_exist(field.data):
            raise StopValidation('Duplicated room name')
        else:
            return form


class UploadForm(FlaskForm):
    files = MultipleFileField('files', validators=[InputRequired()], render_kw={
                              "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, text/csv"})
    room_name = StringField('Room name', validators=[
                            InputRequired(), CheckRoomIdExisted()], render_kw={"placeholder": "Enter room name"})
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), CheckUsernameExisted()], render_kw={"placeholder": "Enter username"})
    password = PasswordField('Password', validators=[InputRequired()], render_kw={"placeholder": "Enter password"})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField('Submit')



class SignInForm(FlaskForm):
    login_username = StringField('Username', validators=[InputRequired()], render_kw={"placeholder": "Enter username"})
    password = PasswordField('Password', validators=[InputRequired()], render_kw={"placeholder": "Enter password"})
    submit = SubmitField('Submit')
    