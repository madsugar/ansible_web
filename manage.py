from app import create_app
from flask_script import Server, Manager, Shell

app = create_app()
manager = Manager(app=app)


def make_shell_context():
    return dict(app=app)


manager.add_command('runserver', Server(host='192.168.1.30', port=80, use_debugger=True, use_reloader=True))

if __name__ == '__main__':
    manager.run(default_command='runserver')
    # manager.run(default_command='shell')
