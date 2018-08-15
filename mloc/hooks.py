from bson import ObjectId
from flask import abort

from model_manager import model_compile, model_fit, model_evaluate, model_predict
from settings import BACKEND


def setup_hooks(app):
    def find_item(resource, item_id):
        items = app.data.driver.db[resource]
        item = items.find_one({'_id': ObjectId(item_id)})
        if not item:
            abort(404)
        return item

    def pre_post_networks(request):
        network = request.get_json()
        if '_id' not in network:
            network['_id'] = ObjectId()
        BACKEND.execute(model_compile, network)

    def pre_post_fits(request):
        data = request.get_json()
        if '_id' not in data:
            data['_id'] = ObjectId()
        network = find_item('networks', data['network_id'])
        BACKEND.execute(model_fit, network=network, **data)

    def pre_post_evaluations(request):
        data = request.get_json()
        fit = find_item('fits', data['fit_id']) 
        network = find_item('networks', fit['network_id'])
        BACKEND.execute(model_evaluate, network=network, **data)

    def pre_post_predictions(request):
        data = request.get_json()
        fit = find_item('fits', data['fit_id']) 
        network = find_item('networks', fit['network_id'])
        BACKEND.execute(model_predict, network=network, **data)

    app.on_pre_POST_networks += pre_post_networks
    app.on_pre_POST_fits += pre_post_fits
    app.on_pre_POST_predictions += pre_post_predictions
    app.on_pre_POST_evaluations += pre_post_evaluations
