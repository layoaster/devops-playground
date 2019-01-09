import logging

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import ignore_logger, LoggingIntegration

# Sentry init
sentry_sdk.init(
    dsn="https://57dfece6e28444129722496518b66bc4@sentry.io/1367700",
    integrations=[
        FlaskIntegration(),
        LoggingIntegration(level='DEBUG'),
    ]
)
ignore_logger("werkzeug")


# Logging config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
