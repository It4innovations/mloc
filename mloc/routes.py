from flask import request, jsonify, abort
from bson import ObjectId

from model_manager import model_fit, model_evaluate, model_predict


def setup_routes(app):
    def find_network(id):
        networks = app.data.driver.db['networks']
        network = networks.find_one({"_id": ObjectId(id)})
        if not network:
            abort(404)
        return network

    @app.route('/networks/<id>/fit', methods=['POST'])
    def network_fit(id):
        network = find_network(id)
        spec = request.get_json()
        model_fit(network, **spec)
        return jsonify({'success': True})

    @app.route('/networks/<id>/evaluate', methods=['POST'])
    def network_evaluate(id):
        network = find_network(id)
        spec = request.get_json()
        result = model_evaluate(network, **spec)
        return jsonify({'success': True, 'result': result})

    @app.route('/networks/<id>/predict', methods=['POST'])
    def network_predict(id):
        network = find_network(id)
        spec = request.get_json()
        result = model_predict(network, **spec)
        return jsonify({'success': True, 'result': result})
