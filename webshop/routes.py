def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('components', '/components')
    config.add_route('orders', '/orders')
    config.add_route('order_create', '/orders/create')
