from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful.utils import cors
from sastocsv.index import sasConvert

app = Flask(__name__)
api = Api(app)


class SasToCsv(Resource):
    @cors.crossdomain(origin='*')
    def post(self):
        data = request.get_json()
        bucket = data['bucket']
        key = data['key']
        convFunc = sasConvert(bucket, key)
        return convFunc


api.add_resource(SasToCsv, '/SasToCsv')

app.run(host='0.0.0.0', port=5000, debug=True)
