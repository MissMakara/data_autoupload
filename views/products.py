import json

from flask import current_app, request
from flask_restful import Resource
from sqlalchemy.sql import text as sql_text

from urllib import response

from db.connection import Db

class Products(Resource):
    def __init__(self):
        self.log = current_app.logger
        self.log.info("Initializing Orders app...")
        self.db = Db()
        self.db_engine = self.db.db_engine
        self.connection = self.db_engine.connect()


    def __del__(self):
        self.log.info("Destroying Orders App ...")
        if self.configs:
            self.configs = None
        
        if self.connection:
            self.db.close()

        if self.db_session:
            self.db_session.remove()

        if self.db:
            self.db.close()

    def get(self, reqparam):
        message = request.args.to_dict()
        self.log.info("Received a GET request")
        response = self.router(reqparam, message)
        return response
    
    def post(self, reqparam):
        products_data = request.get_json()
        self.log.info("Received a POST request, with data,{}".format(products_data))
        response = self.router(reqparam, products_data)
        return response

    def router(self, reqparam, message):
        if reqparam =="add_products":
            response = self.add_products(message)
            return response
        
    



