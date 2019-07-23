from marshmallow import fields
from marshmallow import Schema
from marshmallow import validate


class ProfileSchema(Schema):
    id = fields.UUID()
    email = fields.Email(
        required=True,
        validate=[
            validate.Email(),
            validate.Length(max=128),
        ]
    )
    password = fields.String(
        load_only=True,
        required=True,
        validate=[
            validate.Length(min=8, max=128),
        ],
    )
    created_at = fields.DateTime(dump_only=True)
