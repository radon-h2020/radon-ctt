#!/usr/bin/env python3

import connexion
import logging.config
import traceback
import yaml

from flask import current_app, jsonify

from openapi_server import encoder
from db_orm.database import init_db, db_session
from waitress import serve

# logging.basicConfig(level=logging.INFO)
logging.config.dictConfig(yaml.load(open('logging.conf'), Loader=yaml.SafeLoader))
logfile = logging.getLogger('file')
logconsole = logging.getLogger('console')
logwaitress = logging.getLogger('waitress')

logfile.debug("Debug FILE")
logconsole.info("Info CONSOLE")
logwaitress.info("Info WAITRESS")

app = connexion.App(__name__, specification_dir='./openapi/')
flask_app = app.app


def main():
    init_db()
    # app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'RADON CTT Server API'},
                pythonic_params=True)
    serve(app=app, host="0.0.0.0", port=18080)
    db_session.remove()


@flask_app.errorhandler(Exception)
def handle_exception(error):
    stacktrace = traceback.format_exc()
    current_app.logger.debug(stacktrace)
    try:
        # When a custom error is raised (e.g., CttError)
        response_dict = error.to_dict()
    except AttributeError:
        # When a basic error is raised (e.g., LookupError, ValueError)
        response_dict = {'message': error.args[0],
                         'python_error_class': str(type(error)).split("\'")[1]}
    response = jsonify(response_dict)
    response.status_code = 500
    return response


# from util.errors import CttException
# raise CttException("This is test exception",
#                    payload={'details': {'path': __name__,
#                                         'params': {
#                                             'name': name,
#                                             'repository_url': repository_url}}})

if __name__ == '__main__':
    main()
