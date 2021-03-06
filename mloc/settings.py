import logging
import os

SERVER_PORT = int(os.environ.get("MLOC_PORT", 5000))
AUTH_TOKEN_EXPIRATION_SEC = int(os.environ.get("MLOC_AUTH_TOKEN_EXP", 3600))

LOG_DIR = os.environ.get("MLOC_LOG_DIR", ".")
DEBUG = int(os.environ.get("MLOC_DEBUG", 0))
if DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DBNAME = os.environ.get("MONGO_DBNAME", "test")
MONGO_USERNAME = os.environ.get("MONGO_USERNAME", "")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "")


PBS_SSH_PORT = int(os.environ.get("PBS_SSH_PORT", 22))
PBS_SSH_USERNAME = os.environ.get("PBS_SSH_USERNAME", None)
PBS_HOSTNAME = os.environ.get("PBS_HOSTNAME", None)
PBS_SSH_KEY_PATH = os.environ.get("PBS_SSH_KEY_PATH", None)
PBS_SSH_KEY_PASSWORD = os.environ.get("PBS_SSH_KEY_PASSWORD", None)


HEAPPE_USERNAME = os.environ.get("HEAPPE_USERNAME", None)
HEAPPE_PASSWORD = os.environ.get("HEAPPE_PASSWORD", None)


user_schema = {
    "username": {
        "type": "string",
        "required": True,
        "empty": False,
        "unique": True
    },
    "password": {
        "type": "string",
        "empty": False,
        "required": True
    }
}

layer_schema = {
    "type": "dict",
    "schema": {
        "layer": {
            "type": "string",
            "required": True
        },
        "kwargs": {
            "type": "dict",
            "required": True,
        }
    }
}

network_schema = {
    "_id": {
        "type": "objectid",
        "required": False,
        "empty": False,
        "unique": True
    },
    "name": {
        "type": "string",
        "required": True,
        "empty": False
    },
    "layers": {
        "type": "list",
        "required": True,
        "empty": False,
        "schema": layer_schema
    },
    "state": {
        "type": "string",
        "readonly": True
    },
    "loss": {
        "type": "string",
        "required": True,
        "empty": False
    },
    "optimizer": {
        "type": "string",
        "required": True,
        "empty": False
    },
    "metrics": {
        "type": "list",
        "required": True,
        "empty": False
    },
    "model": {
        "type": "string",
        "required": True,
        "empty": False
    },
    "error": {
        "type": "string",
        "readonly": True
    },
    "result": {
        "type": "string",
        "readonly": True
    }
}

fit_schema = {
    "_id": {
        "type": "objectid",
        "required": False,
        "empty": False,
        "unique": True
    },
    "state": {
        "type": "string",
        "readonly": True
    },
    "network_id": {
        "type": "objectid",
        "data_relation": {
            "resource": "networks",
            "field": "_id",
            "embeddable": True
        },
        "required": True,
        "empty": False
    },
    "x": {
        "type": "list",
        "required": True,
        "empty": False
    },
    "y": {
        "type": "list",
        "required": True,
        "empty": False
    },
    "epochs": {
        "type": "integer",
        "required": False,
        "empty": False
    },
    "batch_size": {
        "type": "integer",
        "required": False,
        "empty": False
    },
    "error": {
        "type": "string",
        "readonly": True
    },
    "result": {
        "type": "string",
        "readonly": True
    },
    "backend": {
        "type": "string",
        "required": True,
        "allowed": ["local", "pbs", "heappe"]
    }
}

evaluation_schema = {
    "fit_id": {
        "type": "objectid",
        "data_relation": {
            "resource": "fits",
            "field": "_id",
            "embeddable": True
        },
        "required": True,
        "empty": False
    },
    "state": {
        "type": "string",
        "readonly": True
    },
    "x": {
        "type": "list",
        "required": True,
        "empty": False
    },
    "y": {
        "type": "list",
        "required": True,
        "empty": False
    },
    "batch_size": {
        "type": "integer",
        "required": False,
        "empty": False
    },
    "error": {
        "type": "string",
        "readonly": True
    },
    "result": {
        "type": "string",
        "readonly": True
    }
}

prediction_schema = {
    "fit_id": {
        "type": "objectid",
        "data_relation": {
            "resource": "fits",
            "field": "_id",
            "embeddable": True
        },
        "required": True,
        "empty": False
    },
    "state": {
        "type": "string",
        "readonly": True
    },
    "x": {
        "type": "list",
        "required": True,
        "empty": False
    },
    "batch_size": {
        "type": "integer",
        "required": False,
        "empty": False
    },
    "error": {
        "type": "string",
        "readonly": True
    },
    "result": {
        "type": "string",
        "readonly": True
    }
}

DOMAIN = {
    "users": {
        "resource_methods": ["GET", "POST"],
        "schema": user_schema,
        "authentication": None,
    },
    "networks": {
        "schema": network_schema,
        "resource_methods": ["GET", "POST"],
        "item_methods": ["GET", "DELETE"],
    },
    "fits": {
        "schema": fit_schema,
        "resource_methods": ["GET", "POST"],
        "item_methods": ["GET", "DELETE"],
    },
    "evaluations": {
        "schema": evaluation_schema,
        "resource_methods": ["GET", "POST"],
        "item_methods": ["GET", "DELETE"],
    },
    "predictions": {
        "schema": prediction_schema,
        "resource_methods": ["GET", "POST"],
        "item_methods": ["GET", "DELETE"],
    }
}
