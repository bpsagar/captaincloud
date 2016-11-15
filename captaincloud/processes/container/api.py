import json
from bottle import Bottle, request
from captaincloud.task import Task

app = Bottle()


@app.route('/submit/', method='POST')
def submit():
    """View to accept a serialized Task and creates a run ID and adds the
    task to a queue"""
    task_dict = json.loads(request.forms.get('task'))
    task = Task.deserialize(data=task_dict)
    run_id = app.config['task_runner'].add(task=task)
    return {'status': 'OK', 'run_id': run_id}


@app.route('/status/', method='POST')
def status():
    """View that returns the status of a Task"""
    run_id = request.forms.get('run_id')
    status = app.config['task_runner'].get_status(run_id=run_id)
    return {'status': 'OK', 'task_status': status}
