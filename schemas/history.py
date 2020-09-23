from marshmallow import Schema, fields, validate


class HistorySchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    task_id = fields.Integer(required=True)
    task_title = fields.String(required=True, validation=[validate.Length(max=128)])
    type = fields.String(required=True, validation=[validate.Length(max=32)])
    status = fields.String(required=True, validation=[validate.Length(max=16)])
    start = fields.DateTime(required=True)
    end = fields.DateTime(required=True)
    txn_date = fields.Date(required=True)
    utc_offset = fields.Integer(required=True)
