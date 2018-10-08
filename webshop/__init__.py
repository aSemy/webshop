from pyramid.config import Configurator

from .util.jsonhelpers import custom_json_renderer

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')

    config.add_renderer('json2', custom_json_renderer())

    config.scan()
    return config.make_wsgi_app()
