import json
import pandas as pd
import csv

from flask import current_app, make_response, request, render_template, redirect, url_for
from flask_restful import Resource
from sqlalchemy.sql import text as sql_text

from urllib import response

from db.connection import Db

class Products(Resource):
    def __init__(self):
        self.log = current_app.logger
        self.log.info("Initializing Products app...")
        self.db = Db()
        self.db_engine = self.db.db_engine
        self.connection = self.db_engine.connect()


    def __del__(self):
        self.log.info("Destroying Products App ...")

        if self.connection:
            self.db.close()

        if self.db:
            self.db.close()

    def get(self, reqparam):
        message = request.args.to_dict()
        self.log.info("Received a GET request")
        response = self.router(reqparam)
        return response
    
    def post(self, reqparam):
        self.log.info("Received a POST request")
        response = self.router(reqparam)
            
        # self.log.info("Received a POST request, with data,{}".format(products_data))
        # response = self.router(reqparam, products_file)
        return response

    def router(self,reqparam):
        if reqparam =="process_file":
            response = self.process_file()
            return response
        
        if reqparam == "upload":
            response = self.launch_form()
            return response       
    
    def process_file(self):
        #convert the file to consise usable data
        try:
            products_file = request.files['file']
            if products_file.filename != '':
                print(products_file)
            
            else:
                response = self.launch_form()
                return response
            
            data = pd.read_csv(products_file, encoding='latin')
            records= data.to_dict('records')
            # print(records)

            return records
        
        except Exception as e:
            self.log.error("Unable to process due to: {}".format(e))
            return e   

    def launch_form(self):   
        headers = {
            'Content-Type': 'text/html'
        }

        return make_response(render_template('upload.html'), 200, headers)
    
    def add_data(self, data):
        return ("in add data method")



