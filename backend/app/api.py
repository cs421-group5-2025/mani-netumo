from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_restx import Api, Resource, fields
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.target import TargetModel

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
jwt = JWTManager(app)
api = Api(app, title='Mini-Netumo API', description='Website monitoring API')

ns = api.namespace('targets', description='Target operations')

target_model = api.model('Target', {
    'url': fields.String(required=True, description='Target URL'),
    'status': fields.String(description='Current status'),
    'latency': fields.Float(description='Response latency in ms'),
    'last_checked': fields.DateTime(description='Last check timestamp')
})

@ns.route('/')
class TargetList(Resource):
    @jwt_required()
    @ns.doc('list_targets')
    @ns.marshal_list_with(target_model)
    def get(self):
        try:
            return [t.to_dict() for t in TargetModel.get_all()]
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    @ns.doc('create_target')
    @ns.expect(target_model)
    def post(self):
        try:
            data = api.payload
            target = TargetModel(url=data['url'])
            target.save()
            return {'message': 'Target created'}, 201
        except Exception as e:
            return {'error': str(e)}, 400

@app.route('/login', methods=['POST'])
def login():
    try:
        access_token = create_access_token(identity='user')
        return jsonify(access_token=access_token)
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)