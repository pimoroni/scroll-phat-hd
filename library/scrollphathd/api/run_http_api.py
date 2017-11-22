from .http import scrollphathd_blueprint
from Flask import Flask
from argparse import ArgumentParser
import scrollphathd
from scrollphathd.fonts import font3x5


def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="HTTP port.", default=8080)
    parser.add_argument("-H", "--host", type=str, help="HTTP host.", default="0.0.0.0")
    args = parser.parse_args()

    scrollphathd.set_clear_on_exit(False)
    scrollphathd.set_brightness(0.1)

    scrollphathd.write_string(str(args.port), font=font3x5, x=1, y=1)
    scrollphathd.show()
    app = Flask(__name__)
    app.register_blueprint(scrollphathd_blueprint, url_prefix="scrollphathd")
    app.run(port=args.port, host=args.host)

if __name__ == '__main__':
    main()