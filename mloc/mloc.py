import eve
import os
import logging

from .hooks import setup_hooks
from .routes import setup_routes
from .db import setup_db_hooks
from .auth import Authenticator
from .settings import LOG_DIR, LOG_LEVEL
from .settings import SERVER_PORT


def run_mloc():
    logging.basicConfig(
        filename=os.path.join(LOG_DIR, 'mloc.log'), level=LOG_LEVEL)
    logging.info('Starting MLOC')

    app = eve.Eve(auth=Authenticator)
    setup_hooks(app)
    setup_routes(app)
    setup_db_hooks(app)
    app.run(threaded=False, host='0.0.0.0', port=SERVER_PORT)
