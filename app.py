from flask import Flask, request, jsonify
from models.task import Task

# __name__ = "__main__"
app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control

    data = request.get_json()
    task = Task(task_id_control, data['title'], data.get('description', ''))

    task_id_control += 1
    tasks.append(task)

    return jsonify({
        'message': 'Nova tarefa criada com sucesso.',
        'id': task.id
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    formatted_tasks = [task.to_dict() for task in tasks]

    return jsonify({
        'tasks': formatted_tasks,
        'total_tasks': len(formatted_tasks)
    })

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):

    for t in tasks:
        if t.id == id:
            return jsonify({
                'task': t.to_dict()
            })
        
    return jsonify({
        'message': 'Não foi possível encontrar a atividade.'
    }), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None

    for t in tasks:
        if t.id == id:
            task = t

    if task == None:
        return jsonify({
            'message': 'Não foi possível encontrar a atividade.'
        }), 404

    task.title = request.get_json().get('title', task.title)
    task.description = request.get_json().get('description', task.description)
    task.completed = request.get_json().get('completed', task.completed)

    return jsonify({
        'message': 'Tarefa atualizada com sucesso.'
    })

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None

    for t in tasks:
        if t.id == id:
            task = t
            break
            
    if task == None:
        return jsonify({
            'message': 'Não foi possível encontrar a atividade'
        }), 404
    
    tasks.remove(task)

    return jsonify({
        'message': 'Tarefa excluída com sucesso.'
    })
    


if __name__ == "__main__":
    app.run(debug=True)