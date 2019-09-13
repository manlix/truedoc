import re

from marshmallow import EXCLUDE
from marshmallow import fields
from marshmallow import post_load
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


class AuthenticationSchema(Schema):
    """Authentication schema."""
    email = fields.Email(required=True, load_only=True, validate=[validate.Length(max=128), validate.Email()])
    password = fields.String(required=True, load_only=True)


class AuthorizationTokensSchema(Schema):
    """Authorization tokens schema."""
    access_token = fields.String(required=True, validate=[validate.Length(min=1)])  # TODO: add regexp for JWT
    refresh_token = fields.String(required=True, validate=[validate.Length(min=1)])  # TODO: add regexp for JWT


class AuthorizationHeaderSchema(Schema):
    """Authorization header schema.
    Common header format: 'Authorization: Bearer ${TOKEN}'.
    See RFC: https://tools.ietf.org/html/rfc6750#section-2.1"""

    class Meta:
        # Exclude unknown fields: https://marshmallow.readthedocs.io/en/stable/quickstart.html#handling-unknown-fields
        unknown = EXCLUDE

    # Check header 'Authorization' for format: 'Bearer ${TOKEN}'.
    Authorization = fields.String(required=True, validate=[validate.Regexp(re.compile('^Bearer (.*\..*\..*)$'))])

    @post_load
    def parts(self, data, **kwargs):
        authorization_schema, token = data['Authorization'].split(' ', maxsplit=1)
        return {
            **data,
            'token': token,
            'authorization_schema': authorization_schema,
        }
