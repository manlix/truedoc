from marshmallow import fields
from marshmallow import Schema
from marshmallow import validate


class ProfileSchema(Schema):
    profile_id = fields.UUID(required=True, dump_only=True)
    email = fields.Email(required=True, validate=[validate.Length(max=128)])
    password = fields.String(required=True, load_only=True, validate=[validate.Length(min=8)])
    created_at = fields.DateTime(required=True, dump_only=True)


class DocumentSchema(Schema):
    """Document schema. Do NOT use UUID for members with 'load_only=True'
    because SQLAlchemy cannot insert value 'UUID(...)' to database."""
    document_id = fields.UUID(required=True, dump_only=True)
    profile_id = fields.String(required=True, load_only=True, validate=[validate.Length(36)])
    title = fields.String(required=True)
    document = fields.Raw(required=True, load_only=True)
    filename = fields.String(required=True)
    filesize = fields.Integer(required=True, validate=[validate.Range(min=0)])
    digest = fields.String(required=True, validate=[validate.Length(equal=32)])
    created_at = fields.DateTime(required=True, dump_only=True)
