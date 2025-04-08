import pytest
import requests

BASE_URL = 'http://localhost:5000'
tasks = []

@pytest.mark.create
def test_create_task():
    task_payload = {
        'title': 'Nova tarefa',
        'description': 'Descrição da nova tarefa'
    }

    response = requests.post(f"{BASE_URL}/tasks", json=task_payload)
    assert response.status_code == 200
    json = response.json()
    assert 'message' in json
    assert 'id' in json
    tasks.append(json['id'])

@pytest.mark.readAll
def test_get_tasks():
    response = requests.get(f'{BASE_URL}/tasks')

    assert response.status_code == 200

    json = response.json()
    
    assert 'tasks' in json
    assert 'total_tasks' in json

@pytest.mark.getTask
def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')

        assert response.status_code == 200

        json = response.json()

        assert task_id == json['task']['id']

@pytest.mark.updateTask
def test_update_task():
    if tasks:
        task_id = tasks[0]
        task_payload = {
            'completed': True
        }
        response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=task_payload)

        assert response.status_code == 200
        json = response.json()
        assert 'message' in json

        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        json = response.json()
        assert json['task']['completed'] == task_payload['completed']

@pytest.mark.deleteTask
def test_delete_tasks():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f'{BASE_URL}/tasks/{task_id}')

        assert response.status_code == 200

        json = response.json()
        
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')

        assert response.status_code == 404