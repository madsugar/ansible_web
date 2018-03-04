from flask import Flask


def create_app():
    app = Flask(__name__)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .api_1_0 import api_1_0 as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api_1_0')

    return app