from flask import Blueprint
from flask import request

from truedoc.db import db
from truedoc.db import schemas
from truedoc.decorators import require_valid_token
from truedoc.response import success

import truedoc.website.context

bp = Blueprint('bookmytime', __name__)


@bp.route('/', methods=['POST'])
@require_valid_token
def date_create():
    """Create new date."""

    profile_id = truedoc.website.context.get("token")["profile_id"]

    date_schema = schemas.BookmytimeDateSchema()

    data = request.get_json()
    data.update({
        'profile_id': profile_id,
    })

    date = db.models.BookmytimeDate(profile_id, data['date'])
    db.BookmytimeDay.create(date)

    return success(result=date_schema.dump(date))


@bp.route('/<uuid:date_id>', methods=['POST'])
@require_valid_token
def time_create(date_id):
    """Create time in the day."""

    date_id = str(date_id)
    profile_id = truedoc.website.context.get("token")["profile_id"]

    data = request.get_json()
    data.update({
        'date_id': date_id,
    })

    time_schema = schemas.BookmytimeTimeSchema()
    data = time_schema.load(data)

    time = db.models.BookmytimeTime(date_id, data['time'])
    db.BookmytimeSlot.create(time, profile_id=profile_id)

    return success(result=time_schema.dump(time))
