import logging

from .backends import LocalBackend
from .db import Database
from .model_manager import (model_compile, model_evaluate, model_fit,
                            model_predict)
from .pbs import PBS


def setup_hooks(app):
    with app.app_context():
        BACKEND = LocalBackend(Database.from_app(app))

    def post_post_networks(request, payload):
        response = payload.get_json()
        logging.debug(
            'triggered post POST networks: {} {}'.format(request, response))
        if response['_status'] == 'OK':
            network = request.get_json()
            BACKEND.execute(model_compile, _id=response['_id'],
                            resource='networks', network=network)
        return payload

    def post_post_fits(request, payload):
        response = payload.get_json()
        logging.debug(
            'triggered post POST fits: {} {}'.format(request, response))
        if response['_status'] == 'OK':
            data = request.get_json()
            if data['backend'] == 'local':
                if '_id' in data:
                    del data['_id']
                db = Database.from_app(app)
                network = db.find_item_by_id('networks', data['network_id'])
                BACKEND.execute(model_fit, _id=response['_id'],
                                resource='fits', network=network, **data)
            elif data['backend'] == 'pbs':
                BACKEND.execute_pbs(PBS.submit_fit, _id=response['_id'],
                                    resource='fits' **data)
        return payload

    def post_post_evaluations(request, payload):
        response = payload.get_json()
        logging.debug(
            'triggered post POST evaluations: {} {}'.format(request, response))
        if response['_status'] == 'OK':
            data = request.get_json()
            if '_id' in data:
                del data['_id']
            db = Database.from_app(app)
            fit = db.find_item_by_id('fits', data['fit_id'])
            network = db.find_item_by_id('networks', fit['network_id'])
            BACKEND.execute(
                model_evaluate, model_json=fit['model_json'],
                model_weights=fit['model_weights'], _id=response['_id'],
                resource='evaluations', network=network, **data)
        return payload

    def post_post_predictions(request, payload):
        response = payload.get_json()
        logging.debug(
            'triggered post POST predictions: {} {}'.format(request, response))
        if response['_status'] == 'OK':
            data = request.get_json()
            if '_id' in data:
                del data['_id']
            db = Database.from_app(app)
            fit = db.find_item_by_id('fits', data['fit_id'])
            network = db.find_item_by_id('networks', fit['network_id'])
            BACKEND.execute(
                model_predict, model_json=fit['model_json'],
                model_weights=fit['model_weights'], _id=response['_id'],
                resource='predictions', network=network, **data)
        return payload

    app.on_post_POST_networks += post_post_networks
    app.on_post_POST_fits += post_post_fits
    app.on_post_POST_predictions += post_post_predictions
    app.on_post_POST_evaluations += post_post_evaluations
