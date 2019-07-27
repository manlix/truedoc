from marshmallow import fields
from marshmallow import Schema
from marshmallow import validate


class ProfileSchema(Schema):
    id = fields.UUID(dump_only=True)
    email = fields.Email(required=True, validate=[validate.Length(max=128)])
    password = fields.String(load_only=True, required=True, validate=[validate.Length(min=8)])
    created_at = fields.DateTime(dump_only=True)
