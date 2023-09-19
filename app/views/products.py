#imports
import json
import pandas as pd
import csv
import magic


from flask import current_app, make_response, Blueprint,request, flash, render_template, redirect, url_for, jsonify
from flask_restful import Resource
from sqlalchemy import select
from sqlalchemy.sql import text as sql_text
from sqlalchemy.exc import SQLAlchemyError
from urllib import response

#import the db connection class
from db.connection import Db

products_blueprint = Blueprint('products', __name__)


class Products(Resource):
    
    #constructor
    def __init__(self):
        #initialize logging
        self.log = current_app.logger
        self.log.info("Initializing Products app...")
        
        #instantiate the class
        self.db = Db()

        #call the db_engine method to create a connection to the db
        self.db_engine = self.db.db_engine
        self.connection = self.db_engine.connect()
        

    #destructor
    def __del__(self):
        self.log.info("Destroying Products App ...")

        if self.connection:
            self.db.close()

        if self.db:
            self.db.close()
    
    #get request handler
    def get(self, reqparam):
        message = request.args.to_dict()
        self.log.info("Received a GET request")
        #call the router method
        response = self.router(reqparam)
        return response
    
    #post request handler
    def post(self, reqparam):
        self.log.info("Received a POST request")
        #call the router method
        response = self.router(reqparam)
            
        # self.log.info("Received a POST request, with data,{}".format(products_data))
        # response = self.router(reqparam, products_file)
        return response

    def router(self,reqparam):
        #if the request received was to process_file
        #call the process file method
        if reqparam =="process_file":
            response = self.process_file()
            return response
        
        #if the request qas to upload
        #launch the upload form
        if reqparam == "upload":
            response = self.launch_form()
            return response     

    
    #the method to launch the upload form
    # @products_blueprint.route('/products/upload', methods=['GET'])
    def launch_form(self, message=None, category=None):   
        headers = {
            'Content-Type': 'text/html'
        }
        if message !=None:
            flash(message, category)
        
        return make_response(render_template('upload.html'), 200, headers)


    #the method to process the uploaded file
    def process_file(self):
        self.log.info("In process file method")
    
        try:
            self.log.info("checking the received file")

            #receive the file
            products_file = request.files['file']
            #check if it is not empty
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
                self.log.info("Reloading form...")
                # response = jsonify({'message': 'No file received.Kindly retry the upload process.'}), 400
                message = "No file received, please upload a csv file"
                category = 'warning'
                # flash(message, category)

                return self.launch_form(message, category)
            
            data = pd.read_csv(products_file, encoding='latin')
            records= data.to_dict('records')
          
            response = self.add_data(records)

            return response
        
        except Exception as e:
            self.log.error("Unable to process due to: {}".format(e))
            return e   

    
    #method to add data to the database
    def add_data(self, data):
        self.log.info("in add data method")
        # self.log.info("Received payload: {}".format(data))

        #create a list to hold the final data
        final_list=[]
        
        #loop through the rows in the uploaded csv file
        for item in data:
            print(item)

            billing_account= item.get('billing_account')
            #check if the billing account value is available
            if billing_account is None:
                message = "UPLOAD ERROR: Billing account column not available."
                category = 'danger'
                flash(message, category)

                return self.launch_form()
                

            
            self.log.info("Running the business_id query")
            #run the query to get the business_id
            business_id_query = "SELECT business_id from business where billing_account = :billing_account"
            try:
                bus_id_resp = self.connection.execute(sql_text(business_id_query),item).fetchone()
            
            #handle any sql error that may occur
            except Exception as error:
                self.log.error("SQL ERROR: {}".format(error))
                message = "QUERY ERROR. Check logs for details or contact your administrator"
                category = 'danger'
                flash(message, category)
                return self.launch_form()
 
            
            #handle any error in getting an output from the query
            if bus_id_resp is None:
                self.log.error("Query returned NULL: {}".format(bus_id_resp))
                message = "Query unsuccessful. Contact your administrator."
                category = 'danger'
                flash(message, category)

                return self.launch_form()
             
            
            business_id_dict =dict(bus_id_resp)
            business_id = business_id_dict["business_id"]
            self.log.info("Received business_id: {}".format(business_id))

            #run the query to get the reference id
            self.log.info("Running the reference id query")
            refno_query = "SELECT count(reference_number) AS count from product where business_id = :business_id"
            try: 
                refno_resp = self.connection.execute(sql_text(refno_query ),business_id_dict).fetchone()
            except Exception as error:
                self.log.error("SQL ERROR: {}".format(error))   
                message = "QUERY ERROR. Check logs for details or contact your administrator"
                category = 'danger'
                flash(message, category)
                return self.launch_form()
            
        
            if refno_resp is None:
                self.log.error("Query returned NULL: {}".format(refno_resp))
                message = "Query unsuccessful. Contact your administrator."
                category = 'danger'
                flash(message, category)
                return self.launch_form()
            
            refno_dict =dict(refno_resp)
            reference_number = refno_dict["count"]+1
            self.log.info("Received reference_number: {}".format(reference_number))

            #GET THE VENDOR_ID
            self.log.info("Running the vendor_id query")
            vendor_name = item.get("vendor_name")
            #check if the vendor_name is present, if not return an error
            if vendor_name == None:
                message = "UPLOAD ERROR: Vendor name not received."
                category = 'danger'
                flash(message, category)
                return self.launch_form()

            #create a dict to hold the vendor_name and the business_id
            vendor_data= {
                "vendor_name":vendor_name,
                "business_id":business_id,
            }               

            self.log.info("Created the vendor dict", vendor_data)
            #run the query to get the vendor_id
            vendor_id_query = "SELECT vendor_id FROM vendor WHERE vendor_name=:vendor_name and business_id=:business_id"
            vendor_resp = self.connection.execute(sql_text(vendor_id_query),vendor_data).fetchone()
            vendor_id_dict =dict(vendor_resp)
            vendor_id = vendor_id_dict["vendor_id"]

            self.log.info("Received vendor_id: {}".format(vendor_id))


            #GET THE UOM_ID
            self.log.info("Running the uom_id query")
            
            #check if the uom_name is present, if not return an error
            uom_name = item.get("uom_name")
            if uom_name == None:
                message = "UPLOAD ERROR: uom name not received."
                category = 'danger'
                flash(message, category)
                
                return self.launch_form()
              
            
            #create a dict to hold the data for the query
            uom_data= {
                "uom_name":uom_name,
                "business_id":business_id,
            }
            self.log.info("Created the uom info dict", uom_data)

            #run the query to get the uom_id
            uom_id_query = "SELECT uom_id FROM uom WHERE uom_name =:uom_name and business_id =:business_id"
            try:
                uom_id_resp = self.connection.execute(sql_text(uom_id_query),uom_data).fetchone()
            
            except Exception as error:
                self.log.error("SQL ERROR: {}".format(error))
                message = "QUERY ERROR. Check logs for details or contact your administrator"
                category = 'danger'
                flash(message, category)
                return self.launch_form()
            
            if uom_id_resp is None:
                self.log.error("Query returned NULL: {}".format(uom_id_resp))
                message = "Query unsuccessful. Contact your administrator."
                category = 'danger'
                flash(message, category)
                return self.launch_form()
            
            uom_dict = dict(uom_id_resp)
            uom_id = uom_dict["uom_id"]
            
            self.log.info("Received uom_id: {}".format(uom_id))
            
        
            #GET THE EXPENSE_GROUP_ID
            self.log.info("Running the expense_data_id query")
            
            #check if the expense_group_name is present, if not return an error
            expense_group_name = item.get("expense_group_name")
            if expense_group_name == None:
                message = "UPLOAD ERROR: expense group name not received."
                category = 'danger'
                flash(message, category)    
                return self.launch_form()
    

            #create the expense_group data to b euse in the query
            expense_data= {
                "expense_group_name":expense_group_name,
                "business_id":business_id,
            }
            
            #run the query
            expense_group_id_query = "SELECT expense_group_id FROM expense_group WHERE group_name= :expense_group_name and business_id=:business_id"
            try:
                expense_group_id_resp = self.connection.execute(sql_text(expense_group_id_query),expense_data).fetchone()
            
            except Exception as error:
                self.log.error("SQL ERROR: {}".format(error))
                message = "QUERY ERROR. Check logs for details or contact your administrator"
                category = 'danger'
                flash(message, category)
                return self.launch_form()
            
            if expense_group_id_resp is None:
                self.log.error("Query returned NULL: {}".format(expense_group_id_query))
                message = "Query unsuccessful. Contact your administrator."
                category = 'danger'
                flash(message, category)
                return self.launch_form()
            
        
            #handle the query output
            expense_group_dict=dict(expense_group_id_resp)
            expense_group_id = expense_group_dict["expense_group_id"]

            self.log.info("Received expense_group_id: {}".format(expense_group_id))


            #GET THE PRODUCT_GROUP_ID
            self.log.info("Running the product_group_id query")

            #check if the product_group_name is present, if not return an error
            product_group_name = item.get("product_group_name")
            if product_group_name == None:
                message = "UPLOAD ERROR: product group name not received."
                category = 'danger'
                flash(message, category)    
                return self.launch_form()

            
            #create a dict to hold the query data
            product_group_data={
                "product_group_name":item["product_group_name"],
                "business_id":business_id,
            }

            #run the query
            product_group_id_query = "SELECT product_group_id FROM product_group WHERE group_name=:product_group_name and business_id=:business_id"
            try:
                product_group_id_resp = self.connection.execute(sql_text(product_group_id_query),product_group_data).fetchone()
            
            except Exception as error:
                self.log.error("SQL ERROR: {}".format(error))
                message = "QUERY ERROR. Check logs for details or contact your administrator"
                category = 'danger'
                flash(message, category)
                return self.launch_form()

            
            if product_group_id_resp is None:
                self.log.error("Product Group Query returned NULL: {}".format(product_group_id_resp))
                message = "Query unsuccessful. Contact your administrator."
                category = 'danger'
                flash(message, category)
                return self.launch_form()
            
            
            product_group_dict = dict(product_group_id_resp)
            product_group_id  = product_group_dict["product_group_id"]
            
            self.log.info("Received product_group_id: {}".format(product_group_id))


            final_data={
                "business_id": business_id,
                "reference_number": reference_number,
                "product_name": item.get("product_name"), 
                "product_code":item.get("product_code"),
                "cost":item.get("cost"),
                "price":item.get("price"),
                "allow_purchase":item.get("allow_purchase"),
                "vendor_id": vendor_id,
                "uom_id": uom_id,
                "expense_group_id": expense_group_id,
                "product_group_id":product_group_id,
                "allow_sale":item.get("allow_sale"), 
                "track_inventory":item.get("track_inventory"),
            
            }

            self.log.info("Received final data dict: {}".format(final_data))

            final_insert ="INSERT INTO product (reference_number, business_id , product_name, product_code, cost, price, allow_purchase, allow_sale, track_inventory, vendor_id, uom_id, expense_group_id, product_group_id) "\
            "VALUES (:reference_number,:business_id,:product_name, :product_code, :cost, :price, :allow_purchase, :allow_sale, :track_inventory, :vendor_id,:uom_id , :expense_group_id, :product_group_id)"
           
            try:
                self.log.info("running the insert query...")
                response = self.connection.execute(sql_text(final_insert),final_data)
            
            except Exception as error:
                self.log.error("SQL ERROR: {}".format(error))
                message= "Insert unsuccessful. Talk to your administrator"
                category ='success'
                flash(message, category)
                return self.launch_form()
             
            #get the id to the last inserted record
            last_insert_query =self.connection.execute("SELECT LAST_INSERT_ID() as last_inserted_id")
            last_insert_id = last_insert_query.scalar()
            self.log.info("Insert successful. Last row_id {}".format(last_insert_id))

            if self.connection is not None:
                self.connection.close()

            message="Success! File data uploaded successfully!"
            category ='success'
            flash(message, category)
            return self.launch_form()
            

            # Close the database connection
     
            

