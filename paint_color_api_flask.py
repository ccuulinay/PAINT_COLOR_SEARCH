from flask import request, abort
from flask import Flask
from flask import jsonify
import random
import logging
import os
import pathlib

from paint_colors import paint_color_helper

APP_NAME = "paint_color_app_flask"

################### Get logger ###################
# set up basic config - logging to console
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s: %(name)s: %(message)s',
                    # datefmt='%m-%d %H:%M',
                    # filename='/temp/myapp.log',
                    # filemode='w'
                    )

# Create console handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_format = logging.Formatter('%(levelname)s: %(asctime)s: %(name)s: %(message)s')
c_handler.setFormatter(c_format)

# Create file handler
log_f_path = os.environ.get("APP_LOG_PATH", os.path.dirname(__file__))
log_f_p = pathlib.Path(log_f_path) / "logs"
log_f_p.mkdir(parents=True, exist_ok=True)
log_f = log_f_p / "app_flask.log"
f_handler = logging.FileHandler(log_f)
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter('%(levelname)s: %(asctime)s: %(name)s: %(message)s')
f_handler.setFormatter(f_format)

# Add hanlder to root logger.
logging.getLogger('').addHandler(f_handler)

# Create a custom logger
logger = logging.getLogger(APP_NAME)

logger.setLevel(logging.INFO)

app = Flask(APP_NAME)


@app.route("/paintcolor/<colorid>", methods=["GET"])
def get_color_by_id(colorid: str):
    c = paint_color_helper.get_color_by_id(colorid)
    return jsonify(c)


@app.route("/paintcolor/all", methods=["GET", "POST"])
def get_all_paint_colors():
    c = paint_color_helper.get_all_paint_colors()
    return jsonify(c)


@app.route("/paintcolor/nearest_colors_by_id", methods=["GET", "POST"])
def get_topk_nearest_paint_colors_by_id():
    if request.method == 'POST':
        data = request.get_json()
        color_id = data.get("color_id")
        if color_id:
            top_k = data.get("top_k", 3)
            r_msg = paint_color_helper.get_nearest_colors_by_id(color_id, top_k)
            # print(r_msg)
            return jsonify(r_msg)
        else:
            r_msg = {
                "message": "request invalid."
            }
            return jsonify(r_msg)

    elif request.method == 'GET':
        data = request.args
        color_id = data.get("color_id")
        if color_id:
            top_k = data.get("top_k", 3)
            r_msg = paint_color_helper.get_nearest_colors_by_id(color_id, top_k)
            # print(r_msg)
            return jsonify(r_msg)
        else:
            r_msg = {
                "message": "request invalid."
            }
            return jsonify(r_msg)
    else:
        return abort(403)


@app.route("/paintcolor/nearest_colors_by_rgb", methods=["GET", "POST"])
def get_topk_nearest_paint_colors_by_rgb():
    if request.method == 'POST':
        data = request.get_json()
        try:
            r = float(data.get("R", 0))
            g = float(data.get("G", 0))
            b = float(data.get("B", 0))
        except Exception as e:
            r_msg = {
                "message": "R, G, B must be integer or float."
            }
            return jsonify(r_msg)
        top_k = data.get("top_k", 3)
        r_msg = paint_color_helper.get_nearest_colors_by_rgb(r, g, b, top_k)
        # print(r_msg)
        return jsonify(r_msg)

    elif request.method == 'GET':
        data = request.args
        try:
            r = float(data.get("R", 0))
            g = float(data.get("G", 0))
            b = float(data.get("B", 0))
        except Exception as e:
            r_msg = {
                "message": "R, G, B must be integer or float."
            }
            return jsonify(r_msg)
        # print(r, g, b)
        top_k = data.get("top_k", 3)
        r_msg = paint_color_helper.get_nearest_colors_by_rgb(r, g, b, top_k)
        return jsonify(r_msg)
    else:
        return abort(403)


@app.route("/ping", methods=['GET'])
def pong():
    pop = ["pong", "oop!"]
    r = random.choices(population=pop, weights=[0.8, 0.2], k=1)
    return r[0]


@app.route("/")
def index():
    return "你好"


@app.route('/mirror_parse', methods=['GET', 'POST'])
def mirror_parse():
    if request.method == 'POST':
        return post_call(request)
    elif request.method == 'GET':
        return get_call(request)


def post_call(req):
    data = req.get_json()
    print(data)
    return jsonify(data)


def get_call(req):
    args = req.args
    print(args)
    return str(args)


@app.before_request
def before_request_func():
    logger.info("before_request is running!")


@app.after_request
def after_request_func(response):
    msg = {
        "app_name": APP_NAME,
        "req_method": request.method,
        "req_json_data": request.get_json(),
        "req_args": request.args,
        "res_status_code": response.status_code,
        "resp_data": response.get_data(),
        "res_json_data": response.get_json(),
    }
    logger.debug(f"AFTER REQUEST: {msg}")
    paint_color_helper.save_paint_color_api_audit_log(msg)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10086, debug=True, threaded=True, )

