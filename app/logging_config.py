import logging
import logging.config

def configure_logging():
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,  # Ensure existing loggers are not blocked
        'formatters': {
            'standard': {
                'format': '[%(levelname)s] %(name)s:%(lineno)d: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',  # Ensure handler can capture DEBUG logs
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            '': {  # Root Logger
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            },
            'app.core.security': {  # Module-Specific Logger
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': False  # Prevent log bubbling
            },
            'app.core.auth': {  # 🔥 Explicitly add `app.core.auth`
                'handlers': ['default'],
                'level': 'DEBUG',  # Enable DEBUG logs
                'propagate': False
            },
        }
    }
    
    logging.config.dictConfig(logging_config)

# Configure logging
configure_logging()

# # Test Logging
# logger = logging.getLogger("app.core.security")
# logger.debug("This is a DEBUG log from app.core.security")  # Should appear
# logger.info("This is an INFO log from app.core.security")  # Should appear

# root_logger = logging.getLogger()
# root_logger.info("This is an INFO log from root")  # Should appear
# root_logger.debug("This DEBUG log should NOT appear")  # Should be filtered

