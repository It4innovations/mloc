import logging
import os


LOG_DIR = os.environ.get('MLOC_LOG_DIR', '.')
DEBUG = int(os.environ.get('MLOC_DEBUG', 0))
if DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO


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
        'empty': False,
        'unique': True
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
    },
    'error': {
        'type': 'string',
        'readonly': True
    },
    'result': {
        'type': 'string',
        'readonly': True
    }
}

fit_schema = {
    '_id': {
        'type': 'objectid',
        'required': False,
        'empty': False,
        'unique': True
    },
    'state': {
        'type': 'string',
        'readonly': True
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
    },
    'error': {
        'type': 'string',
        'readonly': True
    },
    'result': {
        'type': 'string',
        'readonly': True
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
    'state': {
        'type': 'string',
        'readonly': True
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
    },
    'error': {
        'type': 'string',
        'readonly': True
    },
    'result': {
        'type': 'string',
        'readonly': True
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
    'state': {
        'type': 'string',
        'readonly': True
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
    },
    'error': {
        'type': 'string',
        'readonly': True
    },
    'result': {
        'type': 'string',
        'readonly': True
    }
}

DOMAIN = {
    'users': {
        'resource_methods': ['GET', 'POST'],
        'schema': user_schema,
        'authentication': None,
    },
    'networks': {
        'schema': network_schema,
        'resource_methods': ['GET', 'POST'],
        'item_methods': ['GET', 'DELETE'],
    },
    'fits': {
        'schema': fit_schema,
        'resource_methods': ['GET', 'POST'],
        'item_methods': ['GET', 'DELETE'],
    },
    'evaluations': {
        'schema': evaluation_schema,
        'resource_methods': ['GET', 'POST'],
        'item_methods': ['GET', 'DELETE'],
    },
    'predictions': {
        'schema': prediction_schema,
        'resource_methods': ['GET', 'POST'],
        'item_methods': ['GET', 'DELETE'],
    }
}
