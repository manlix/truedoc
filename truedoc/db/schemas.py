import re

import datetime

from marshmallow import EXCLUDE
from marshmallow import fields
from marshmallow import post_dump
from marshmallow import post_load
from marshmallow import Schema
from marshmallow import validate
from marshmallow import validates
from marshmallow import ValidationError

import truedoc.constants
import truedoc.config


class ProfileSchema(Schema):
    profile_id = fields.UUID(required=True, dump_only=True)
    email = fields.Email(required=True, validate=[validate.Length(max=128)])
    password = fields.String(required=True, load_only=True, validate=[validate.Length(min=8)])
    created_at = fields.DateTime(required=True, dump_only=True)


class DocumentSchema(Schema):
    """Base schema for Document."""
    document_id = fields.String(required=True, validate=[validate.Length(36)])
    profile_id = fields.String(required=True, validate=[validate.Length(36)])
    title = fields.String(required=True)
    filename = fields.String(required=True)

    filesize = fields.Integer(validate=[validate.Range(min=1, max=truedoc.config.PROJECT.MAX_DOCUMENT_FILESIZE)])
    digest = fields.String(validate=[validate.Length(equal=32)])
    created_at = fields.DateTime()

    state = fields.String(
        required=True,
        validate=[validate.OneOf(choices=truedoc.constants.JOB_STATE.ALL_STATES)],
    )


class AuthenticationSchema(Schema):
    """Authentication schema."""
    email = fields.Email(required=True, load_only=True)  # ATTENTION: do NOT use validator for 'email' for type 'Email'
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


class BookmytimeDateSchema(Schema):
    """Boookmytime 'Date' schema."""
    date_id = fields.String(required=True, dump_only=True, validate=[validate.Length(36)])
    profile_id = fields.String(required=True, load_only=True, validate=[validate.Length(36)])
    date = fields.Date(required=True)


class BookmytimeTimeSchema(Schema):
    """Bookmytime 'Time' schema."""
    time_id = fields.String(required=True, dump_only=True, validate=[validate.Length(36)])
    date_id = fields.String(required=True, load_only=True, validate=[validate.Length(36)])
    time = fields.String(required=True, validate=[
        validate.Regexp(re.compile('^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'), error="Incorrect time"),
    ])

    @post_dump
    def parts(self, data, **kwargs):
        data.update({
            'time': data['time'][0:5],  # Format data from db: '13:00:00' -> '13:00'
        })
        return data
