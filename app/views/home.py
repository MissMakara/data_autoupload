from flask import current_app, render_template

def index():
    # return "Welcome to auto upload API "
    return render_template('index.html')