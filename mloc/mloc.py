import eve

from hooks import setup_hooks
from routes import setup_routes
from db import setup_db_hooks
from auth import Authenticator


app = eve.Eve(auth=Authenticator)
setup_hooks(app)
setup_routes(app)
setup_db_hooks(app)
app.run(threaded=False, host='0.0.0.0')
