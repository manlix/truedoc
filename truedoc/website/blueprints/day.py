from flask import Blueprint
from flask import request

from truedoc.db import db
from truedoc.db import schemas
from truedoc.decorators import require_valid_token
from truedoc.response import success

import truedoc.website.context

bp = Blueprint('day', __name__)


@bp.route('/', methods=['POST'])
@require_valid_token
def days():
    """Create new day."""

    profile_id = truedoc.website.context.get("token")["profile_id"]

    day_schema = schemas.DaySchema()
    data = day_schema.load(request.get_json())

    day = db.models.Day(profile_id, data['date'])
    db.Day.create(day)

    return success()
