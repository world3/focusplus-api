from marshmallow import Schema, fields, validate


class StatSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    stat_key = fields.String(dump_only=True)
    pomos = fields.String(dump_only=True)
    breaks = fields.String(dump_only=True)
    totalPomos = fields.Integer(dump_only=True)
    totalBreaks = fields.Integer(dump_only=True)
    interruptions = fields.Integer(dump_only=True)
