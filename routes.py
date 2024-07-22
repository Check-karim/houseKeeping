from flask import Blueprint,render_template,request,flash,session,redirect,jsonify,make_response
# from controller.user import add_user_function,edit_user_function
import sys
from models.models import User
# from helper import generic_helper,db_helper
# from controller import chat,order as order_function

main = Blueprint('main', __name__ ) #routename= main


@main.route('/', methods = ['GET'])
def home():
    return render_template("index.html")