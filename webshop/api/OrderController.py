from pyramid.response import Response
from pyramid.view import view_config

from datetime import datetime

from sqlalchemy.exc import DBAPIError

from ..models import (Order)

import logging
log = logging.getLogger(__name__)

#
# @view_config(context=Order)
# class OrderEndpoints(object):
#     def __init__(self, context, request):
#         self.request = request
#         self.context = context
#         self.view_name = 'OrderEndpoints'


@view_config(request_method='GET', route_name='orders', renderer='json2')
def order_view(request):
    try:
        query = request.dbsession.query(Order)
    except DBAPIError as e:
        log.error(str(e))
        return Response("Database error", content_type='text/plain', status=500)
    return query.all()


@view_config(request_method='PUT', route_name='order_create', renderer='json2')
def order_create(request):
    try:
        log.info("Trying to create an Order. Input: %s" % request.json_body)

        # read from request
        # create order
        new_order = Order(
            client_id=request.json_body['client_id'],
            preferred_delivery_datetime=datetime.now().replace(microsecond=0))

        # TODO validate: order's components are valid

        request.dbsession.add(new_order)
    except DBAPIError as e:
        log.error(str(e))
        return Response("Database error", content_type='text/plain', status=500)
    return Response(status=200)
