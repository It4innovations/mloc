from model_manager import model_compile, model_fit, \
    model_evaluate, model_predict, model_build
from backends import LocalBackend
from db import Database


def setup_hooks(app):
    with app.app_context():
        BACKEND = LocalBackend(Database(app))

    def post_post_networks(request, payload):
        response = payload.get_json()
        if response['_status'] == 'OK':
            network = request.get_json()
            BACKEND.execute(model_compile, _id=response['_id'],
                            resource='networks', network=network)
        return payload

    def post_post_fits(request, payload):
        response = payload.get_json()
        if response['_status'] == 'OK':
            data = request.get_json()
            if '_id' in data:
                del data['_id']
            db = Database(app)
            network = db.find_item_by_id('networks', data['network_id'])
            BACKEND.execute(model_fit, _id=response['_id'],
                            resource='fits', network=network, **data)
        return payload

    def post_post_evaluations(request, payload):
        response = payload.get_json()
        if response['_status'] == 'OK':
            data = request.get_json()
            if '_id' in data:
                del data['_id']
            db = Database(app)
            fit = db.find_item_by_id('fits', data['fit_id'])
            network = db.find_item_by_id('networks', fit['network_id'])
            model = model_build(fit['model_json'], fit['model_weights'])
            BACKEND.execute(model_evaluate, model=model, _id=response['_id'],
                            resource='evaluations', network=network, **data)
        return payload

    def post_post_predictions(request, payload):
        response = payload.get_json()
        if response['_status'] == 'OK':
            data = request.get_json()
            if '_id' in data:
                del data['_id']
            db = Database(app)
            fit = db.find_item_by_id('fits', data['fit_id'])
            network = db.find_item_by_id('networks', fit['network_id'])
            model = model_build(fit['model_json'], fit['model_weights'])
            BACKEND.execute(model_predict, model=model, _id=response['_id'],
                            resource='predictions', network=network, **data)
        return payload

    app.on_post_POST_networks += post_post_networks
    app.on_post_POST_fits += post_post_fits
    app.on_post_POST_predictions += post_post_predictions
    app.on_post_POST_evaluations += post_post_evaluations
