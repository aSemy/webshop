from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import (Order)

import logging
log = logging.getLogger(__name__)


@view_config(route_name='orders', renderer='json')
def my_view(request):
    try:
        query = request.dbsession.query(Order)
    except DBAPIError as e:
        log.error(str(e))
        return Response("Database error", content_type='text/plain', status=500)
    return query.all()
