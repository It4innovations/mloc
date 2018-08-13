from flask import request, jsonify
from bson import ObjectId

from model_manager import model_init, model_fit, model_evaluate, model_predict


def setup_routes(app):
    def find_network(id):
        networks = app.data.driver.db['networks']
        network = networks.find_one({"_id": ObjectId(id)})
        return network

    @app.route('/networks/<id>/init', methods=['POST'])
    def network_init(id):
        network = find_network(id)
        if not network:
            return 404
        model_init(network)
        return jsonify({'success': True})

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
