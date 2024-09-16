import anvil.server


def register_api_service(name, description, url, connection_type='in'):
    return anvil.server.call('register_api_service', name, description, url, connection_type)
