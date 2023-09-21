from pathlib import Path
from flask_wtf import FlaskForm
from wtforms.fields import StringField, MultipleFileField, SubmitField
from wtforms.validators import InputRequired, StopValidation
from store import room_name

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


class CheckRoomIdExisted(object):
    def __init__(self, message=None):
        self.message = message

    def __check_room_exist(self, room_to_check):
        return room_to_check in room_name

    def __call__(self, form, field):
        if self.__check_room_exist(field.data):
            raise StopValidation('Duplicated room name')
        else:
            return


class UploadForm(FlaskForm):
    files = MultipleFileField('files', validators=[InputRequired(), MultiFileAllowed(['.csv', '.xlsx'])], render_kw={
                              "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, text/csv"})
    room_name = StringField('Room name', validators=[
                            InputRequired(), CheckRoomIdExisted()], render_kw={"placeholder": "Enter room name"})
    submit = SubmitField('Submit')