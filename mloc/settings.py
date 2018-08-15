user_schema = {
    'username': {
        'type': 'string',
        'required': True,
        'empty': False,
        'unique': True
    },
    'password': {
        'type': 'string',
        'empty': False,
        'required': True
    }
}

layer_schema = {
    'type': 'dict',
    'schema': {
        'layer': {
            'type': 'string',
            'required': True
        },
        'kwargs': {
            'type': 'dict',
            'required': True,
        }
    }
}

network_schema = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'layers': {
        'type': 'list',
        'required': True,
        'empty': False,
        'schema': layer_schema
    },
    'state': {
        'type': 'string',
        'readonly': True
    },
    'loss': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'optimizer': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'metrics': {
        'type': 'list',
        'required': True,
        'empty': False
    },
    'model': {
        'type': 'string',
        'required': True,
        'empty': False
    }
}


DOMAIN = {
    'users': {
        'schema': user_schema,
        'resource_methods': ['GET', 'POST'],
        'item_methods': ['GET', 'DELETE']
    },
    'networks': {
        'schema': network_schema,
        'resource_methods': ['GET', 'POST'],
        'item_methods': ['GET', 'DELETE']
    }
}
