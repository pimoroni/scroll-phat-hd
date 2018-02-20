import time
import signal

import scrollphathd

from argparse import ArgumentParser

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

try:
    from queue import Empty
except ImportError:
    from Queue import Empty

from .action import Action
from .stoppablethread import StoppableThread

try:
    import http.client as http_status
except ImportError:
    import httplib as http_status

from flask import Blueprint, render_template, abort, request, jsonify, Flask

scrollphathd_blueprint = Blueprint('scrollhat', __name__)
api_queue = Queue()

# To handle automatic scroll
auto_scroll = False

@scrollphathd_blueprint.route('/scroll', methods=["POST"])
def scroll():
    response = {"result": "success"}
    status_code = http_status.OK

    data = request.get_json()
    if data is None:
        data = request.form
    try:
        api_queue.put(Action("scroll", (int(data["x"]), int(data["y"]))))
    except KeyError:
        response = {"result": "KeyError", "error": "keys x and y not posted."}
        status_code = http_status.UNPROCESSABLE_ENTITY
    except ValueError:
        response = {"result": "ValueError", "error": "invalid integer."}
        status_code = http_status.UNPROCESSABLE_ENTITY

    return jsonify(response), status_code


@scrollphathd_blueprint.route('/show', methods=["POST"])
def show():
    global auto_scroll

    response = {"result": "success"}
    status_code = http_status.OK

    data = request.get_json()
    if data is None:
        data = request.form
    # Update global auto_scroll value
    if data["auto_scroll"] == "True":
        auto_scroll = True
    else:
        auto_scroll = False
    try:
        api_queue.put(Action("write", data["text"]))
    except KeyError:
        response = {"result": "KeyError", "error": "key 'text' not set"}
        status_code = http_status.UNPROCESSABLE_ENTITY

    return jsonify(response), status_code


@scrollphathd_blueprint.route('/clear', methods=["POST"])
def clear():
    response = {"result": "success"}
    status_code = http_status.OK

    api_queue.put(Action("clear", {}))
    return jsonify(response), status_code


@scrollphathd_blueprint.route('/flip', methods=["POST"])
def flip():
    response = {"result": "success"}
    status_code = http_status.OK

    data = request.get_json()
    if data is None:
        data = request.form
    try:
        api_queue.put(Action("flip", (bool(data["x"]), bool(data["y"]))))
    except TypeError:
        response = {"result": "TypeError", "error": "Could not cast data correctly. Both `x` and `y` must be set to true or false."}
        status_code = http_status.UNPROCESSABLE_ENTITY
    except KeyError:
        response = {"result": "KeyError", "error": "Could not cast data correctly. Both `x` and `y` must be in the posted json data."}
        status_code = http_status.UNPROCESSABLE_ENTITY

    return jsonify(response), status_code


def run():
    while True:
        global auto_scroll

        try:
            action = api_queue.get(block=False, timeout=1)

            if action.action_type == "write":
                # Clear the buffer before writing new text
                scrollphathd.clear()
                scrollphathd.write_string(action.data)

            if action.action_type == "clear":
                scrollphathd.clear()

            if action.action_type == "scroll":
                scrollphathd.scroll(action.data[0], action.data[1])

            if action.action_type == "flip":
                scrollphathd.flip(x=action.data[0], y=action.data[1])
        except Empty:
            pass

        scrollphathd.show()

        if auto_scroll is True:
            scrollphathd.scroll()
            time.sleep(0.1)


def start_background_thread():
    api_thread = StoppableThread(target=run)
    api_thread.start()


scrollphathd_blueprint.before_app_first_request(start_background_thread)


def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="HTTP port.", default=8080)
    parser.add_argument("-H", "--host", type=str, help="HTTP host.", default="0.0.0.0")
    args = parser.parse_args()

    scrollphathd.set_clear_on_exit(False)
    # To check if it is visible!
    scrollphathd.set_brightness(0.1)

    scrollphathd.write_string(str(args.port), x=1, y=1)
    scrollphathd.show()
    app = Flask(__name__)
    app.register_blueprint(scrollphathd_blueprint, url_prefix="/scrollphathd")
    app.run(port=args.port, host=args.host)


if __name__ == '__main__':
    main()
