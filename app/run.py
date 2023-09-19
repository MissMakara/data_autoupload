import logging.handlers

from flask import Flask, request, redirect, url_for, current_app
from flask_restful import Api
from concurrent_log_handler import ConcurrentRotatingFileHandler
import os

from views.home import index
from views.products import Products
from utils.utilsfile import ConfigsParser as config
from os.path import join, dirname, realpath
# from views.products import products_blueprint

configs = config.parse_configs('BASE')

handler = ConcurrentRotatingFileHandler(configs.get('log_file'), "a", 1024 * 1024 * 1024 * 1, 1000)
formatter = logging.Formatter(
    '%(asctime)s] - %(name)s - %(levelname)s in %(module)s:%(lineno)d:%(funcName)-10s %(message)s')
handler.setFormatter(formatter)


app = Flask(__name__, template_folder="templates")
api = Api(app)
app.secret_key = configs.get('secret_key')
app.config['SESSION_TYPE'] = configs.get('session_type')

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Register the products_blueprint with the app
# app.register_blueprint(products_blueprint)


app.add_url_rule("/", view_func=index)
api.add_resource(Products, "/products/<string:reqparam>")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

