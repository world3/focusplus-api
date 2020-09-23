from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from marshmallow import ValidationError

from models.history import History
from schemas.history import HistorySchema

history_schema = HistorySchema()
history_list_schema = HistorySchema(many=True)


class HistoryListResource(Resource):
    @jwt_required
    def get(self, txn_date):
        current_user = get_jwt_identity()
        histories = History.get_by_user_id(current_user, txn_date)
        result = history_list_schema.dump(histories)
        return result, HTTPStatus.OK


class CreateHistoryResource(Resource):
    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        try:
            data = history_schema.load(data=json_data)
        except ValidationError as errors:
            return {'message': 'Validation errors', 'errors': errors.messages}, HTTPStatus.BAD_REQUEST

        history = History(**data)
        history.user_id = current_user
        history.save()

        return history_schema.dump(history), HTTPStatus.CREATED
