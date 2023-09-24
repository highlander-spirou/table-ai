"""
This module contains controllers for HTMX response
"""
from flask import Blueprint, abort, request, flash
from flask_htmx import HTMX
from utils import render_view
from interfaces import *
import pandas as pd
from models import RoomUtils, DataframeUtils, UserUtils

htmx_routes = Blueprint('htmx_routes', __name__,
                        template_folder='templates/htmx_response')
htmx = HTMX(htmx_routes)


@htmx_routes.before_request
def htmx_check_middleware():
    if not htmx:
        print('Force URL in HTMX route')
        abort(404)


@htmx_routes.route('/existing_room')
def check_existing_room():
    q = request.args.get('room_name')
    if q:
        if RoomUtils.find_room(q) is not None:
            props: ExistingRoomInterface = {
                'status': False, 'message': 'Room name exist! Please choose another room name'}
        else:
            props: ExistingRoomInterface = {
                'status': True, 'message': 'Room name valid'}
        return render_view('htmx_response/existing_room.html', props=props)
    else:
        props: ExistingRoomInterface = {
            'status': False, 'message': 'Room name is empty'}
        return render_view('htmx_response/existing_room.html', props=props)


@htmx_routes.route('/get-table')
def get_table():
    room_name = request.args.get('room_name')
    table_name = request.args.get('table_name')

    if room_name is None or table_name is None:
        flash('Error accessing dashboard')
        return abort(404)
    else:
        df = pd.read_parquet(
            f'./uploads/{room_name}/{table_name}.parquet.gzip')
        result = df.iloc[0:5].to_dict('split')
        props: TableInterface = {'result': result,
                                 'table_name': table_name, 'room_name': room_name}

        alias = DataframeUtils.get_alias(room_name, table_name)
        if alias is not None:
            props['alias'] = alias
        return render_view('htmx_response/table.html', props=props)


@htmx_routes.route('/change-alias', methods=['POST'])
def change_alias():
    new_alias, room_name, table_name = [request.form.get(
        i) for i in ('change_alias', 'room_name', 'table_name')]
    DataframeUtils.update_alias(room_name, table_name, new_alias)
    return f'<p>Alias: {new_alias}</p>'


@htmx_routes.route('/existing_username')
def check_existing_username():
    username = request.args.get('username')
    if username:
        if UserUtils.find_user(username) is not None:
            props: ExistingUsernameInterface = {'status': False, 'message': 'Username existed'}
        else:
            props: ExistingUsernameInterface = {'status': True, 'message': 'Username valid'}
    else:
        props: ExistingUsernameInterface = {'status': False, 'message': 'Username empty'}
    return render_view('htmx_response/existing_username.html', props=props)

# @htmx_routes.route('/a/<int:button_id>')
# def confirm_btn_click(button_id:int):
#     btn_clicked = filter_dict_list(li, 'id', button_id)
#     result: BtnResponseInterface = {'label': btn_clicked[0]['label']}
#     return render_view('htmx_response/btn-response.html', result=result)
