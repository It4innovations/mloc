import eve

from routes import setup_routes

app = eve.Eve()
setup_routes(app)
app.run(threaded=False)