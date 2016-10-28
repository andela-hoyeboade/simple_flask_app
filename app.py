#!flask/bin/python
from flask import Flask, abort, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import Task, db

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/api/v1/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def single_task(task_id):
    if request.method == 'GET':
        task = Task.query.filter_by(id=task_id).first()
        if task:
            return jsonify({'task': task.get()})
        abort(404)

    if request.method == 'PUT':
        title = request.json.get('title', '')
        description = request.json.get('description', '')
        done = request.json.get('done', '')
        task = Task.query.filter_by(id=task_id).first()
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if done:
                task.done = done
            task.update()
            return jsonify({'task': task.get()})
        abort(404)

    if request.method == 'DELETE':
        task = Task.query.filter_by(id=task_id).first()
        if task:
            task.delete()
            return jsonify({'message': 'task deleted successfully'})
        else:
            abort(404)


@app.route('/api/v1/tasks', methods=['POST', 'GET'])
def get_or_create_task():
    if request.method == 'GET':
        tasks = Task.query.all()
        return jsonify({'tasks': [task.get() for task in tasks]})
    if request.method == 'POST':
        title = request.json.get('title', '')
        description = request.json.get('description', '')
        if not title:
            abort(400, {'message': 'Title is blank or missing'})
        if not description:
            abort(400, {'message': 'Description is blank or missing'})
        new_task = Task(title=title, description=description)
        new_task.save()
        return jsonify({'task': new_task.get()}), 201


if __name__ == '__main__':
    app.run(debug=True)
