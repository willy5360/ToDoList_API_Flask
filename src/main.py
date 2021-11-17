"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.route('/todos', methods=['GET'])
def get_task():
    tasks = Task.get_all_tasks()
    print("ayudaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",tasks)
    all_tasks = [task.to_dict() for task in tasks]
    print("aqui estoy buscameeeeeeee",all_tasks)
    return jsonify(all_tasks), 200

@app.route('/todos', methods=['POST'])
def create_task():
    new_label = request.json.get('label', None) #Aqui me devuelve lo que escriba en el front en la parte de "label:" y si no lo esribe con none

    if not new_label:
        return jsonify({'error':"Missing task label"}), 400
    task = Task(label = new_label, done = False)
    # try:
    task_created = task.create_new_task()
    return jsonify(task_created.to_dict()), 201    
    # except exc.IntegrityError:
    #     return jsonify({'error':'Fail on load'}), 400

@app.route('/todos/<int:id>' , methods=['PATCH'])
def set_task_finished(id):
    task = Task.get_task_id(id)
    if task:
        task.task_finished()
        return jsonify("Task is done!!!",task.to_dict()), 200
    return jsonify({'error': 'Task not found'}), 400

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete(id):
    task = Task.get_task_id(id)
    if task:
        task.delete_task()
        return jsonify("task eliminated",task.to_dict() ) , 200
    return jsonify({'error': 'Task not found'}), 400


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
