import argparse
from wsgiref.simple_server import make_server
from .container_api import ContainerAPI
from .task_runner import TaskRunner
from captaincloud.utils.http import bottle_api


class Container(object):
    """Container to execute tasks"""

    def __init__(self, host='localhost', port=25000):
        """Create a Task Runner instance and Container API"""
        self.host = host
        self.port = port
        self.task_runner = TaskRunner()
        container_api = ContainerAPI(container=self)
        self.app = bottle_api.make_app(instance=container_api, mount='/api')
        self.server = make_server(self.host, self.port, self.app)

    def run(self):
        """Run the container"""
        self.task_runner.start()
        self.server.serve_forever()
        self.task_runner.join()

    def stop(self):
        """Stop the app"""
        self.server.shutdown()
        self.server.server_close()
        self.task_runner.stop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=25000)
    args = parser.parse_args()
    container = Container(host=args.host, port=args.port)
    try:
        print('Starting container process')
        container.run()
    except KeyboardInterrupt:
        print('Shutting down...')
        container.stop()
