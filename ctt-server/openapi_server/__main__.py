#!/usr/bin/env python3

import connexion
import logging

from openapi_server import encoder
from db_orm.database import init_db, db_session
from waitress import serve

logging.basicConfig(level=logging.INFO)


def main():
    init_db()

    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'RADON CTT Server API'},
                pythonic_params=True)
    #app.run(port=18080)
    serve(app, host="0.0.0.0", port=18080)

    db_session.remove()


if __name__ == '__main__':
    main()

