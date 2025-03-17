# app/logging_config.py
import logging
import logging.config

def configure_logging():
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': True
            },
            'app.routers.ifaceconfig': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': False
            },
            'app.ai.ai_interface': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': False
            },
            'app.ai.common': {  
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }

    logging.config.dictConfig(logging_config)