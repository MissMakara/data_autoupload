import json
import pandas as pd
import csv
import magic

from flask import current_app, make_response, request, flash, render_template, redirect, url_for, jsonify
from flask_restful import Resource
from sqlalchemy import select
from sqlalchemy.sql import text as sql_text
from sqlalchemy.exc import SQLAlchemyError

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

    #the method to process the uploaded file
    def process_file(self):
        self.log.info("In process file method")
        #convert the file to consise usable data
        try:
            self.log.info("checking the received file")

            #receive the file
            products_file = request.files['file']
            if products_file.filename != '':
                self.log.info("It seems a file has been received..")
                self.log.info("Checking the content type...")

                # file_type = magic.from_buffer(products_file.stream.read(), mime=True)
                # if products_file.content_type !='text/csv' or file_type != 'text/csv':

                #check if the file is csv file
                if products_file.content_type !='text/csv':
                    self.log.error("Uploaded file is not a csv file")

                    error_message = "Wrong file format. Please upload a csv file"
                    flash(error_message)

                    # return redirect('/products/upload')
                    
                    # response = make_response("File format not in csv format", 400)
                    #if not launch the upload form
                    
                    return self.launch_form()

            else:
                #check if file has not been received
                self.log.error("File not received")
                flash("No file received, please upload a csv file")
                self.log.info("Reloading form...")
                # response = jsonify({'message': 'No file received.Kindly retry the upload process.'}), 400
                
                return self.launch_form()
            
            data = pd.read_csv(products_file, encoding='latin')
            records= data.to_dict('records')
            # print(records)
            response = self.add_data(records)
            return response
        
        except Exception as e:
            self.log.error("Unable to process due to: {}".format(e))
            return e   

    def launch_form(self):   
        headers = {
            'Content-Type': 'text/html'
        }

        return make_response(render_template('upload.html'), 200, headers)
    
    def add_data(self, data):
        self.log.info("in add data method")
        # self.log.info("Received payload: {}".format(data))

        final_list=[]
        try:

            for item in data:
                print(item)
                business_id_data = {
                    "billing_account": "BA02",
                }
                self.log.info("Running the business_id query")
                business_id_query = "SELECT business_id from business where billing_account = :billing_account"
                try:
                    bus_id_resp = self.connection.execute(sql_text(business_id_query),business_id_data).fetchone()
                
                except SQLAlchemyError as error:
                    self.log.error("SQL ERROR: {}".format(error))
                    return "Query ERROR"

                if bus_id_resp is None:
                    self.log.error("Query returned NULL: {}".format(bus_id_resp))
                    return "Query unsuccessful"
                business_id_dict =dict(bus_id_resp)

                business_id = business_id_dict["business_id"]
                self.log.info("Received business_id: {}".format(business_id))

                
                self.log.info("Running the reference id query")
                refno_query = "SELECT count(reference_number) AS count from product where business_id = :business_id"
                try: 
                    refno_resp = self.connection.execute(sql_text(refno_query ),business_id_dict).fetchone()
                except SQLAlchemyError as error:
                    self.log.error("SQL ERROR: {}".format(error))
                    return "Query ERROR"
            
                if refno_resp is None:
                    self.log.error("Query returned NULL: {}".format(refno_resp))
                    return "Query unsuccessful"
                
                refno_dict =dict(refno_resp)
                # print(refno_dict)
                reference_number = refno_dict["count"]+1
                self.log.info("Received reference_number: {}".format(reference_number))

                # vendor_data= {
                #     "vendor_name":item["vendor_name"],
                #     "business_id":business_id,
                # }

                # vendor_id_query = "SELECT vendor_id FROM vendor WHERE vendor_name=:vendor_name and business_id=:business_id"
                # vendor_resp = self.connection.execute(sql_text(vendor_id_query),vendor_data).fetchone()
                # vendor_id_dict =dict(vendor_resp)
                # vendor_id = vendor_id_dict["vendor_id"]

                # self.log.info("Received vendor_id: {}".format(vendor_id))

                self.log.info("Running the uom_id query")
                uom_data= {
                    "uom_name":item["uom_name"],
                    "business_id":business_id,
                }
                print("UOM_name:", uom_data["uom_name"])

                uom_id_query = "SELECT uom_id FROM uom WHERE uom_name =:uom_name and business_id =:business_id"
                try:
                    uom_id_resp = self.connection.execute(sql_text(uom_id_query),uom_data).fetchone()
                
                except SQLAlchemyError as error:
                    self.log.error("SQL ERROR: {}".format(error))
                    return "Query ERROR"
                
                if uom_id_resp is None:
                    self.log.error("Query returned NULL: {}".format(uom_id_resp))
                    return "Query unsuccessful"
                
                uom_dict = dict(uom_id_resp)
                uom_id = uom_dict["uom_id"]
                
                self.log.info("Received uom_id: {}".format(uom_id))
                


                self.log.info("Running the expense_data_id query")
                expense_data= {
                    "expense_group_name":item["expense_group_name"],
                    "business_id":business_id,
                }
                print(expense_data['expense_group_name'])
                
                expense_group_id_query = "SELECT expense_group_id FROM expense_group WHERE group_name= :expense_group_name and business_id=:business_id"
                try:
                    expense_group_id_resp = self.connection.execute(sql_text(expense_group_id_query),expense_data).fetchone()
                except SQLAlchemyError as error:
                    self.log.error("SQL ERROR: {}".format(error))
                    return "Query ERROR"
                
                if expense_group_id_resp is None:
                    self.log.error("Query returned NULL: {}".format(expense_group_id_query))
                    return "Query unsuccessful"
                
                expense_group_dict=dict(expense_group_id_resp)
                expense_group_id = expense_group_dict["expense_group_id"]

                self.log.info("Received expense_group_id: {}".format(expense_group_id))

                
                self.log.info("Running the product_group_id query")
                product_group_data={
                    "product_group_name":item["product_group_name"],
                    "business_id":business_id,
                }
                print(product_group_data["product_group_name"])

                product_group_id_query = "SELECT product_group_id FROM product_group WHERE group_name=:product_group_name and business_id=:business_id"
                try:
                    product_group_id_resp = self.connection.execute(sql_text(product_group_id_query),product_group_data).fetchone()
                
                except SQLAlchemyError as error:
                    self.log.error("SQL ERROR: {}".format(error))
                
                if product_group_id_resp is None:
                    self.log.error("Product Group Query returned NULL: {}".format(product_group_id_resp))
                    return "Query unsuccessful"
                
                
                product_group_dict = dict(product_group_id_resp)
                product_group_id  = product_group_dict["product_group_id"]
                
                self.log.info("Received product_group_id: {}".format(product_group_id))

                # final_data={
                #     "business_id": business_id,
                #     "product_name": item["product_name"], 
                #     "product_code":item["product_code"],
                #     "cost":item["cost"],
                #     "price":item["price"],
                #     "vendor_id": vendor_id,
                #     "uom_id": uom_id,
                #     "expense_group_id": expense_group_id,
                #     "product_group_id":product_group_data,
                #     # "alert_quantity:"
                #     # "product_type",
                #     # "product_nature", 
                #     "allow_purchase":item["allow_purchase"], 
                #     "allow_sale":item["allow_sale"], 
                #     "notes":item.get["notes"], 
                #     "track_inventory":item["track_inventory"],
                #     # "earn_commission":item["earn_commission"] 
                #     # "media_id", 
                #     # "commission_type_id"

                # }

                
                # final_insert ="INSERT INTO product ('reference_number', 'product_name`, `product_code`, `cost`, `price`, `allow_purchase`, `allow_sale`, `notes`, `track_inventory`, `vendor_id`, `uom_id`, `expense_group_id`, `product_group_id`, `business_id`, `item_status_id`)"\
                # "VALUES (:reference_number,:business_id,:product_name, :product_code, :cost, :price, :allow_purchase, :allow_sale, :notes, :track_inventory, :vendor_id,:uom_id , :expense_group_id, :product_group_id, :item_status_id)"
                
                # response = self.connection.execute(sql_text(final_insert),final_data)

    
        except Exception as e:
            self.log.error("ERROR: {}".format(e))
            s= "ERROR: {}".format(e)
            return s

        finally:
            # Close the database connection
            if self.connection is not None:
                self.connection.close()

        return product_group_id
