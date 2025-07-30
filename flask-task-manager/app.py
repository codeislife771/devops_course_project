from flask import Flask, request, jsonify, render_template, redirect
import json
from datetime import datetime
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'

    
def load_tasks():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)


@app.route('/', methods=['GET'])
def redirect_to_tasks():
    return redirect('/tasks', code=302)

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "ok"}, 200

@app.route('/tasks', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(load_tasks())

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    name = data.get('name')
    author = data.get('author')
    if not name or not author:
        return jsonify({'error': 'Invalid or duplicate task name'}), 400

    tasks = load_tasks()
    tasks[name] = {
        'author': data.get('author', ''),
        'date_create': datetime.now().strftime('%Y-%m-%d')
    }
    save_tasks(tasks)
    return jsonify({'message': 'Task created'}), 201

@app.route('/tasks/<name>', methods=['PUT'])
def update_task(name):
    tasks = load_tasks()
    if name not in tasks:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    tasks[name]['author'] = data.get('author', tasks[name]['author'])
    save_tasks(tasks)
    return jsonify({'message': 'Task updated'}), 200

@app.route('/tasks/<name>', methods=['DELETE'])
def delete_task(name):
    tasks = load_tasks()
    if name in tasks:
        del tasks[name]
        save_tasks(tasks)
        return jsonify({'message': 'Task deleted'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', debug=debug, port=port)
