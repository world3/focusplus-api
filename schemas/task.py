from marshmallow import Schema, fields, validate, validates, ValidationError


class TaskSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validation=[validate.Length(max=128)])
    description = fields.String(allow_none=True, alidation=[validate.Length(max=256)])
    priority = fields.Integer(required=True)
    type = fields.String(required=True, validation=validate.OneOf(['backlog', 'active', 'trash', 'archive']))
    status = fields.String(required=True, validation=[validate.Length(max=32)])
    due_date = fields.Date(required=True)
    start = fields.DateTime(required=False, allow_none=True)
    end = fields.DateTime(required=False, allow_none=True)

    @validates('priority')
    def validate_priority(self, n):
        if n < 1:
            raise ValidationError('Priority number must be greater than 0')
        if n >= 1000:
            raise ValidationError('Priority number must be lower than 1000')
