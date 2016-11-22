import argparse

from captaincloud.utils.http import bottle_api
from wsgiref.simple_server import make_server

from .api import TaskRunnerAPI
from .runner import TaskRunner


class TaskRunnerProcess(object):
    """Process to execute tasks"""

    def __init__(self, host='localhost', port=25000):
        """Create a Task Runner Process"""
        self.host = host
        self.port = port

    def run(self):
        """Run the Process"""
        self.runner = TaskRunner()
        self.runner_api = TaskRunnerAPI(process=self, runner=self.runner)

        self.app = bottle_api.make_app(('/api', self.runner_api))
        self.server = make_server(self.host, self.port, self.app)

        self.runner.start()
        self.server.serve_forever()
        self.runner.join()

    def stop(self):
        """Stop the Process"""
        self.server.shutdown()
        self.server.server_close()
        self.runner.stop()


def main():
    """Entry point for cc-task-runner"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=25000)

    args = parser.parse_args()
    container = TaskRunnerProcess(host=args.host, port=args.port)
    try:
        print('Starting container process')
        container.run()
    except KeyboardInterrupt:
        print('Shutting down...')
        container.stop()
