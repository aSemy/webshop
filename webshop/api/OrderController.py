from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import (Order)

import logging
log = logging.getLogger(__name__)


@view_config(request_method='GET', route_name='orders', renderer='json')
def order_view(request):
    try:
        query = request.dbsession.query(Order)
    except DBAPIError as e:
        log.error(str(e))
        return Response("Database error", content_type='text/plain', status=500)
    return query.all()


@view_config(request_method='PUT', route_name='order_create', renderer='json')
def order_create(request):
    try:
        # read from request
        # create order
        # validate: order's components are valid
        query = request.dbsession.query(Order)
    except DBAPIError as e:
        log.error(str(e))
        return Response("Database error", content_type='text/plain', status=500)
    return query.all()
