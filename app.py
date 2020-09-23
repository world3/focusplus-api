from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extensions import db, jwt

from resources.history import HistoryListResource, CreateHistoryResource
from resources.setting import SettingResource
from resources.stat import StatListResource
from resources.task import TaskListResource, TaskResource
from resources.token import TokenResource, RefreshResource, black_list
from resources.user import UserListResource, UserResource, MeResource


def create_app():
    application = Flask(__name__)
    CORS(application)
    application.config.from_object(Config)
    register_extensions(application)
    register_resources(application)
    return application


def register_extensions(application):
    db.init_app(application)
    migrate = Migrate(application, db)
    jwt.init_app(application)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list


def register_resources(application):
    api = Api(application)
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(StatListResource, '/stat/<string:start>/<string:end>')
    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/token/refresh')
    api.add_resource(TaskListResource, '/tasks/<string:type>')
    api.add_resource(TaskResource, '/tasks/id/<string:task_id>')
    api.add_resource(CreateHistoryResource, '/histories')
    api.add_resource(HistoryListResource, '/histories/<string:txn_date>')
    api.add_resource(SettingResource, '/setting')


if __name__ == '__main__':
    app = create_app()
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    app.run()
