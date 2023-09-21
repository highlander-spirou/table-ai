"""
This module contains controllers for normal HTML views
"""

from flask import Blueprint, request, redirect
import pandas as pd
from interfaces import *
from utils import render_view
from forms import UploadForm

normal_routes = Blueprint('normal_routes', __name__,
                          template_folder='templates')



@normal_routes.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if request.method == 'POST':
        return redirect('/')
        # if form.validate_on_submit():
        #     upload_files = request.files.getlist("files")
        #     request_room_name = request.form.get('room_name')
        #     ensure_path_exist(f'./uploads/{request_room_name}')
        #     for file in upload_files:
        #         if 'sheet' in file.mimetype:
        #             df = pd.read_excel(file)
        #         else:
        #             df = pd.read_csv(file)
        #         df.to_csv(
        #             f'./uploads/{file.filename}.csv')
        #     return redirect('/dashboard')
        # else:
        #     flash('Room existed! Try another room name')
        #     return redirect('/')
    return render_view('index.html', form=form)


@normal_routes.route('/upload', methods=['POST'])
def upload():
    upload_files = request.files.getlist("files")
    print(request.files)
    # request_room_name = request.form.get('room_name')
    # if request_room_name in room_name:
    #     flash('Room existed! Try another room name')
    #     return redirect('/')

    # ensure_path_exist(f'./uploads/{request_room_name}')

    # for file in upload_files:
    #     print(file.filename)
    # if 'sheet' in file.mimetype:
    #     print(f'{file.filename} is an excel file')
    #     df = pd.read_excel(file)
    # else:
    #     print(f'{file.filename} is a csv file')
    #     df = pd.read_csv(file)
    # df.to_parquet(f'./uploads/{request_room_name}/{file.filename}.parquet.gzip', compression='gzip')

    return redirect('/')


@normal_routes.route('/dashboard')
def dashboard():
    return '<p>Dashboard</p>'
