import logging

import connexion
from flask_testing import TestCase
from db_orm.database import init_db, db_session
from openapi_server.encoder import JSONEncoder


class BaseTestCase(TestCase):

    def create_app(self):
        init_db()
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../openapi/')
        app.app.json_encoder = JSONEncoder
        app.add_api('openapi.yaml', pythonic_params=True)
        return app.app
