from pyramid.response import Response
from pyramid.view import view_config

from datetime import datetime

import time

from sqlalchemy.exc import DBAPIError

from sqlalchemy.sql import exists

from ..models import (
    Order,
    Component,
)

import logging

log = logging.getLogger(__name__)

datetime_parse_format = "%Y%m%d_%H%M"  # year_month_day_hour_minute, e.g. 20181231_2359

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

        client_id = request.json_body['client_id']
        delivery_datetime_string = request.json_body.get('preferred_delivery_yyyyMMdd_HHmm')
        component_ids = request.json_body['component_ids']

        # start validating

        # TODO validate delivery date is in future
        if delivery_datetime_string:
            delivery_struct_time = time.strptime(delivery_datetime_string, datetime_parse_format)
            # convert struct_time to datetime
            delivery_datetime = datetime(*delivery_struct_time[:6])
            if not delivery_datetime:
                raise ValueError("Given delivery datetime is invalid: %s" % delivery_datetime_string)
            if delivery_datetime <= datetime.now():
                raise ValueError("Delivery datetime cannot be in past: %s" % delivery_datetime_string)

        # validate components exist
        invalid_component_ids = []
        for component_id in component_ids:
            if not request.dbsession.query(exists().where(Component.id == component_id)).scalar():
                invalid_component_ids.append(component_id)
        if len(invalid_component_ids) > 0:
            raise ValueError("Component IDs do not exist: %s" % invalid_component_ids)

        # finished validating

        delivery_datetime = None
        if delivery_datetime_string:
            delivery_struct_time = time.strptime(delivery_datetime_string, datetime_parse_format)
            # convert struct_time to datetime
            delivery_datetime = datetime(*delivery_struct_time[:6])

        # create order
        new_order = Order()
        new_order.client_id = client_id

        if delivery_datetime:
            new_order.preferred_delivery_datetime = delivery_datetime

        # components to add to this order
        valid_components = []
        # fetch components from the database
        for component_id in component_ids:
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
        return Response("Validation error. %s" % str(e), content_type='text/plain', status=500)
    return Response(status=200)
