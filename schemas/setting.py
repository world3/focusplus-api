from marshmallow import Schema, fields, validate


class SettingSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    key = fields.String(required=True, validation=[validate.Length(max=128)])
    value = fields.String(required=True, alidation=[validate.Length(max=128)])


