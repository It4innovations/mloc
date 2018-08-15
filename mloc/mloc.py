import eve

from routes import setup_routes
from hooks import setup_hooks

app = eve.Eve()
setup_routes(app)
setup_hooks(app)
app.run(threaded=False)
