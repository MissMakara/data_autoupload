from flask import Flask
from flask_restful import Api

from views.home import index
from views.product import 


app = Flask(__name__)
api = Api(app)

app.add_url_rule("/", view_func=index)

api.add_resource(products, "/products/<string:reqparam>")


if __name__ == "__main__":
    app.run(port=5000, debug=True)

