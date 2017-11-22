import scrollphathd
from scrollphathd.fonts import font3x5

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

from .action import Action
from .stoppablethread import StoppableThread

try:
    import http.HTTPStatus as http_status
except ImportError:
    import httplib as http_status

try:
    from flask import Blueprint, render_template, abort, request, jsonify
except ImportError:
    raise ImportError("flask must be installed in order to use the api. Install with pip install flask")

scrollphathd_blueprint = Blueprint('scrollhat', __name__)
api_queue = Queue()

@scrollphathd_blueprint.route('/scroll', methods=["POST"])
def scroll():
    response = {"result": "success"}
    status_code = http_status.OK.value

    data = request.get_json()
    if data is None:
        data = request.form
    try:
        api_queue.put(Action("scroll", (data["x"], data["y"])))
    except KeyError:
        response = {"result": "KeyError", "error": "keys x and y not posted."}
        status_code = http_status.UNPROCESSABLE_ENTITY.value

    return jsonify(response), status_code


@scrollphathd_blueprint.route('/show', methods=["POST"])
def show(text):
    response = {"result": "success"}
    status_code = http_status.OK.value

    data = request.get_json()
    if data is None:
        data = request.form
    try:
        api_queue.put(Action("write", data["text"]))
    except KeyError:
        response = {"result": "KeyError", "error": "key 'text' not set"}
        status_code = http_status.UNPROCESSABLE_ENTITY.value

    return jsonify(response), status_code


@scrollphathd_blueprint.route('/clear', methods=["POST"])
def clear():
    response = {"result": "success"}
    status_code = http_status.OK.value

    api_queue.put(Action("clear", {}))
    return jsonify(response), status_code


@scrollphathd_blueprint.route('/flip', methods=["POST"])
def flip():
    response = {"result": "success"}
    status_code = http_status.OK.value

    data = request.get_json()
    if data is None:
        data = request.form
    try:
        api_queue.put(Action("flip", (bool(data["x"]), bool(data["y"]))))
    except TypeError:
        response = {"result": "TypeError", "error": "Could not cast data correctly. Both `x` and `y` must be set to true or false."}
        status_code = http_status.UNPROCESSABLE_ENTITY.value
    except KeyError:
        response = {"result": "KeyError", "error": "Could not cast data correctly. Both `x` and `y` must be in the posted json data."}
        status_code = http_status.UNPROCESSABLE_ENTITY.value

    return jsonify(response), status_code


def run():
    while True:
        action = api_queue.get(block=True)
        if action.action_type == "write":
            scrollphathd.write_string(action.data, font=font3x5)

        if action.action_type == "clear":
            scrollphathd.clear()

        if action.action_type == "scroll":
            scrollphathd.scroll(action.data[0], action.data[1])

        if action.action_type == "flip":
            scrollphathd.flip(x=action.data[0], y=action.data[1])

        scrollphathd.show()

def start_background_thread():
    api_thread = StoppableThread(target=run)
    api_thread.start()
    
scrollphathd_blueprint.before_app_first_request(start_background_thread)
