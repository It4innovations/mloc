from flask import request
from bson import ObjectId


def setup_routes(app):
    @app.route('/networks/<network_id>/fit', methods=['POST'])
    def network_fit(network_id):
        data = request.get_json()
        pass

    @app.route('/fits/<fit_id>/evaluate', methods=['POST'])
    def fit_evaluate(fit_id):
        data = request.get_json()
        pass

    @app.route('/fits/<fit_id>/predict', methods=['POST'])
    def fit_predict(fit_id):
        data = request.get_json()
        pass

    @app.route('/networks/<network_id>/fits/<fit_id>/evaluate', methods=['POST'])
    def network_fit_evaluate(network_id, fit_id):
        data = request.get_json()
        pass

    @app.route('/networks/<network_id>/fits/<fit_id>/predict', methods=['POST'])
    def network_fit_predict(network_id, fit_id):
        data = request.get_json()
        pass
