import scrollphathd
from scrollphathd.fonts import font3x5
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
from threading import Thread
from .action import Action
from http import HTTPStatus

try:
    from flask import Blueprint, render_template, abort, request
except ImportError:
    raise ImportError("flask must be installed in order to use the api. Install with pip install flask")

scrollphathd_blueprint = Blueprint('scrollhat', __name__)
api_queue = Queue()

@scrollphathd_blueprint.route('/scroll', methods=["POST"])
def scroll():
    data = request.get_json()
    try:
        api_queue.put(Action("scroll", (data["x"], data["y"])))
    except KeyError:
        return {"error": "keys x and y not posted."}, HTTPStatus.UNPROCESSABLE_ENTITY.value
    else:
        return HTTPStatus.OK.value


@scrollphathd_blueprint.route('/show', methods=["POST"])
def show(text):
    data = request.get_json()
    try:
        api_queue.put(Action("write", data["text"]))
    except KeyError:
        return {"error": "key 'text' not set"}, HTTPStatus.UNPROCESSABLE_ENTITY.value
    else:
        return HTTPStatus.OK.value

@scrollphathd_blueprint.route('/clear', methods=["POST"])
def clear():
    api_queue.put(Action("clear", {}))
    return HTTPStatus.OK.value

@scrollphathd_blueprint.route('/flip', methods=["POST"])
def flip():
    data = request.get_json()
    try:
        api_queue.put(Action("flip", (bool(data["x"]), bool(data["y"]))))
    except TypeError:
        return {"error": "Could not cast data correctly. Both `x` and `y` must be set to true or false."}, \
               HTTPStatus.UNPROCESSABLE_ENTITY.value
    else:
        return HTTPStatus.OK.value

def run():
    while True:
        action = api_queue.get(block=True)
        if action.action_type == "write":
            scrollphathd.write_string(action.data, font=font3x5)
            scrollphathd.show()

        if action.action_type == "clear":
            scrollphathd.clear()

        if action.action_type == "scroll":
            scrollphathd.scroll(action.data[0], action.data[1])
            scrollphathd.show()

        if action.action_type == "flip":
            scrollphathd.flip(x=action.data[0], y=action.data[1])

def start_background_thread():
    api_thread = Thread(target=run)
    api_thread.start()
    
scrollphathd_blueprint.before_app_first_request(start_background_thread)
