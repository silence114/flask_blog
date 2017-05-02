from app import create_app
from flask_script import Manager
from models.models import init_db
app = create_app()


if __name__ == '__main__':
    init_db()
    manager = Manager(app)

    @manager.command
    def develop():
        app.run(host='0.0.0.0', port=8080, debug=True)


    @manager.command
    def product():
        app.run(host='0.0.0.0', port=80, debug=False)

    manager.run()


