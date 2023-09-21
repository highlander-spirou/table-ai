"""
This module contains controllers for normal HTML views
"""

from flask import Blueprint, request, redirect, flash
import pandas as pd
from interfaces import *
from utils import render_view, ensure_path_exist, get_filename
from forms import UploadForm

normal_routes = Blueprint('normal_routes', __name__,
                          template_folder='templates')



@normal_routes.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            upload_files = request.files.getlist("files")
            request_room_name = request.form.get('room_name')
            ensure_path_exist(f'./uploads/{request_room_name}')
            for file in upload_files:
                if 'sheet' in file.mimetype:
                    df = pd.read_excel(file)
                else:
                    df = pd.read_csv(file)
                df.to_parquet(f'./uploads/{request_room_name}/{get_filename(file.filename)}.parquet.gzip', compression='gzip')
            return redirect(f'/dashboard?room_name={request_room_name}')
        else:
            flash('Some error occurs, please retry')
            return redirect('/')
    return render_view('index.html', form=form)



@normal_routes.route('/dashboard')
def dashboard():
    request_room_name = request.args.get('room_name')
    return f'<p>Dashboard from {request_room_name}</p>'
