"""
This module contains controllers for normal HTML views
"""

from flask import Blueprint, request, redirect, flash, abort, url_for
import pandas as pd
from interfaces import *
from utils import render_view, get_filename
from forms import UploadForm, SignUpForm, SignInForm
from models import RoomUtils, DataframeUtils, UserUtils
from flask_login import login_user, login_required, logout_user, current_user

normal_routes = Blueprint('normal_routes', __name__,
                          template_folder='templates')


@normal_routes.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            upload_files = request.files.getlist("files")
            room_name = request.form.get('room_name')
            RoomUtils.add_new_room(room_name)

            for file in upload_files:
                if 'sheet' in file.mimetype:
                    df = pd.read_excel(file)
                else:
                    df = pd.read_csv(file)
                parquet_file_path = f'./uploads/{room_name}/{get_filename(file.filename)}.parquet.gzip'
                df.to_parquet(parquet_file_path, compression='gzip')
                DataframeUtils.add_dataframe(
                    room_name, get_filename(file.filename))
            return redirect(f'/dashboard?room_name={room_name}')
        else:
            flash('Some error occurs, please retry')
            return redirect('/')
    return render_view('index.html', form=form)


@normal_routes.route('/dashboard')
@login_required
def dashboard():

    return render_view('dashboard.html')


@normal_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            UserUtils.create_user(request.form.get(
                'username'), request.form.get('password'))
            return redirect('/login')
        else:
            flash('Submit error')
            return redirect('/signup')

    return render_view('signup.html', form=form)


@normal_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    form = SignInForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserUtils.login_user(
                form.login_username.data, form.password.data)
            login_user(user)

            # Redirect to protected route
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                # Default navigate to dashboard on `user_authenticated`
                next = url_for('normal_routes.dashboard')

            return redirect(next)
        else:
            flash('Submit error')
            return redirect('/login')

    return render_view('login.html', form=form)


@normal_routes.route('/test_create_room', methods=['GET', 'POST'])
def test_create_room():
    if UserUtils.find_user('asd') is None:
        UserUtils.create_user('asd', 'asd')
        login_user(UserUtils.find_user('asd'))
    rooms = UserUtils.list_room(current_user.id)
    for room in rooms:
        print(room.name, room.get_dataframe_names())
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        file_name = request.form.get('file_name')
        target_room = RoomUtils.find_room(room_name)
        if target_room is None:
            target_room = RoomUtils.add_new_room(room_name, current_user)
        DataframeUtils.add_dataframe(target_room, file_name)
    return render_view('test_view.html')

# @normal_routes.route('/dashboard')
# def dashboard():
#     room_name = request.args.get('room_name')
#     if room_name is None or RoomUtils.find_room(room_name) is None:
#         flash('Error navigate to dashboard')
#         return abort(404)

#     files = DataframeUtils.list_dataframe_from_room(room_name)
#     files = [i.file_name for i in files]

#     props: DashBoardInterface = {
#         'room_name': room_name, 'files': files, 'title': 'Dashboard'}
#     return render_view('dashboard.html', props=props)
