"""
This module contains controllers for HTMX response
"""
from flask import Blueprint, abort, request
from flask_htmx import HTMX
from utils import render_view
from interfaces import *
from store import room_name


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
        if q in room_name:
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
# @htmx_routes.route('/a/<int:button_id>')
# def confirm_btn_click(button_id:int):
#     btn_clicked = filter_dict_list(li, 'id', button_id)
#     result: BtnResponseInterface = {'label': btn_clicked[0]['label']}
#     return render_view('htmx_response/btn-response.html', result=result)
