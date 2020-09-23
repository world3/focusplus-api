from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from marshmallow import ValidationError

from models.setting import Setting
from schemas.setting import SettingSchema

setting_schema = SettingSchema()
setting_list_schema = SettingSchema(many=True)


class SettingResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        settings = Setting.get_by_user(current_user)
        if settings is None:
            return {'message': 'settings not found'}, HTTPStatus.NOT_FOUND

        result = setting_list_schema.dump(settings)
        return result, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        data = []
        for item in json_data:
            try:
                setting = setting_schema.load(data=item)
                data.append(setting)
            except ValidationError as errors:
                return {'message': 'Validation errors', 'errors': errors.messages}, HTTPStatus.BAD_REQUEST

        settings = Setting.get_by_user(current_user)
        if settings is None:
            settings = []

        update_settings = []
        m = {item.key: item for item in settings}
        for item in data:
            key = item['key']
            value = item['value']
            if key in m:
                setting = m[key]
                setting.value = value
            else:
                setting = Setting(key=key, value=value, user_id=current_user)
            update_settings.append(setting)

        Setting.save(update_settings)

        return setting_list_schema.dump(settings), HTTPStatus.CREATED
