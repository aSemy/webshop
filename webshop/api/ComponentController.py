from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import (Component)


@view_config(route_name='components', renderer='json')
def my_view(request):
    try:
        query = request.dbsession.query(Component)
    except DBAPIError:
        return Response("Database error", content_type='text/plain', status=500)
    return query.all()
