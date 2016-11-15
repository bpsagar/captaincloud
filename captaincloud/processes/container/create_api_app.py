import bottle
from .api import app as api_app


def create_api_app(task_runner):
    """Create container API endpoint"""
    app = bottle.Bottle()
    app.config['task_runner'] = task_runner
    sub_apps = [api_app]
    for sub_app in sub_apps:
        sub_app.config.update({'task_runner': task_runner})
        app.mount('/api', sub_app)
    return app
