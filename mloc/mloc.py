import eve

from hooks import setup_hooks

app = eve.Eve()
setup_hooks(app)
app.run(threaded=False)