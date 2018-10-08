from pyramid.response import Response
from pyramid.view import view_config

from datetime import datetime

from sqlalchemy.exc import DBAPIError

from sqlalchemy.sql import exists

from ..models import (
    Order,
    Component,
)

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
            preferred_delivery_datetime=datetime.now())

        # start validating

        # TODO validate delivery date is in future

        # validate components exist
        invalid_component_ids = []

        # request.dbsession.query(Component.id).filter(exists().where(Component.id == component_id))

        for component_id in request.json_body['component_ids']:
            if not request.dbsession.query(exists().where(Component.id == component_id)).scalar():
                invalid_component_ids.append(component_id)

        #     if not exists().where(Component.id == component_id):
        #         invalid_component_ids.append(component_id)

        if len(invalid_component_ids) > 0:
            raise ValueError("Component IDs do not exist: %s" % invalid_component_ids)

        # finished validating

        # components to add to this order
        valid_components = []
        # fetch components from the database
        for component_id in request.json_body['component_ids']:
            if request.dbsession.query(exists().where(Component.id == component_id)).scalar():
                component = request.dbsession.query(Component).filter_by(id=component_id).first();
                valid_components.append(component)

        # add valid components to the order
        new_order.components.extend(valid_components)

        request.dbsession.add(new_order)
    except DBAPIError as e:
        log.error(str(e))
        return Response("Database error", content_type='text/plain', status=500)
    except ValueError as e:
        log.error(str(e))
        return Response("Component ID error. %s" % str(e), content_type='text/plain', status=500)
    return Response(status=200)
