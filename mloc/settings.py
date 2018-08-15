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
    '_id': {
        'type': 'objectid',
        'required': False,
        'empty': False
    },
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

fit_schema = {
    '_id': {
        'type': 'objectid',
        'required': False,
        'empty': False
    },
    'network_id': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'networks',
            'field': '_id',
            'embeddable': True
        },
        'required': True,
        'empty': False
    },
    'x': {
        'type': 'list',
        'required': True,
        'empty': False
    },
    'y': {
        'type': 'list',
        'required': True,
        'empty': False
    },
    'epochs': {
        'type': 'integer',
        'required': False,
        'empty': False
    },
    'batch_size': {
        'type': 'integer',
        'required': False,
        'empty': False
    }
}

evaluation_schema = {
    'fit_id': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'fits',
            'field': '_id',
            'embeddable': True
        },
        'required': True,
        'empty': False
    },
    'x': {
        'type': 'list',
        'required': True,
        'empty': False
    },
    'y': {
        'type': 'list',
        'required': True,
        'empty': False
    },
    'batch_size': {
        'type': 'integer',
        'required': False,
        'empty': False
    }
}

prediction_schema = {
    'fit_id': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'fits',
            'field': '_id',
            'embeddable': True
        },
        'required': True,
        'empty': False
    },
    'x': {
        'type': 'list',
        'required': True,
        'empty': False
    },
    'batch_size': {
        'type': 'integer',
        'required': False,
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
    },
    'fits': {
        'schema': fit_schema,
        'resource_methods': ['GET', 'POST'],
        'item_methods': ['GET', 'DELETE']
    },
    'evaluations': {
        'schema': evaluation_schema,
        'resource_methods': ['GET', 'POST'],
        'item_methods': ['GET', 'DELETE']
    },
    'predictions': {
        'schema': prediction_schema,
        'resource_methods': ['GET', 'POST'],
        'item_methods': ['GET', 'DELETE']
    }
}