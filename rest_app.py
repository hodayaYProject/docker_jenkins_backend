import jsonpickle
from flask import Flask, request
from db_connector import Stock
from datetime import date
from user import User
import os
import signal

app = Flask(__name__)

@app.route('/stop_server')
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return 'Server stopped'

@app.route('/users/<user_id>', methods=['GET','POST','PUT','DELETE'])
def user(user_id):
    if request.method == 'POST':
        request_data = request.json
        user_name = request_data.get('user_name')
        user = jsonpickle.encode(User((user_id,user_name, date.today())))
        user = Stock.create_user(user)
        if user:
            return {"status": "ok", "user_added": user_name}, 200
        else:
            return {"status": 'error', "reason": "id already exits"}, 500

    elif request.method == 'GET':
        user = Stock.get_user(user_id)
        if user:
            return {"status": "ok", "user_name": user.name}, 200
        else:
            return {"status": 'error', "reason": "no such id"}, 500

    elif request.method == 'PUT':
        request_data = request.json
        user_name = request_data.get('user_name')
        user = jsonpickle.encode(User((user_id,user_name, date.today())))
        user = Stock.update_user(user)
        if user:
            return {"status": "ok", "user_update": user_name}, 200
        else:
            return {"status": 'error', "reason": "no such id"}, 500

    elif request.method == 'DELETE':
        user = Stock.delete_user(user_id)
        if user == 1:
            return {"status": "ok", "user_deleted": user_id}, 200
        else:
            return {"status": 'error', "reason": "no such id"}, 500



app.run(host='0.0.0.0', debug=True, port=5000)