from bson import ObjectId

from model_manager import model_compile, model_fit, model_evaluate, model_predict
from backends import Local
from db import find_item

def setup_hooks(app):
    with app.app_context():
        BACKEND = Local(app.data.driver.db)

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
            network = find_item(app.data.driver.db, 'networks', data['network_id'])
            BACKEND.execute(model_fit, _id=response['_id'],
                            resource='fits', network=network, **data)
        return payload

    def post_post_evaluations(request, payload):
        response = payload.get_json()
        if response['_status'] == 'OK':
            data = request.get_json()
            fit = find_item(app.data.driver.db, 'fits', data['fit_id']) 
            network = find_item(app.data.driver.db, 'networks', fit['network_id'])
            BACKEND.execute(model_evaluate, _id=response['_id'],
                            resource='evaluations', network=network, **data)
        return payload

    def post_post_predictions(request, payload):
        response = payload.get_json()
        if response['_status'] == 'OK':
            data = request.get_json()
            fit = find_item(app.data.driver.db, 'fits', data['fit_id']) 
            network = find_item(app.data.driver.db, 'networks', fit['network_id'])
            BACKEND.execute(model_predict, _id=response['_id'],
                            resource='predictions', network=network, **data)
        return payload

    app.on_post_POST_networks += post_post_networks
    app.on_post_POST_fits += post_post_fits
    app.on_post_POST_predictions += post_post_predictions
    app.on_post_POST_evaluations += post_post_evaluations
