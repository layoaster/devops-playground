"""
Initialization of the application with all required configurations.
"""
import logging
import sys

import sentry_sdk
from pythonjsonlogger import jsonlogger
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import ignore_logger, LoggingIntegration


# Sentry init
sentry_sdk.init(
    dsn="https://57dfece6e28444129722496518b66bc4@sentry.io/1367700",
    integrations=[FlaskIntegration(), LoggingIntegration(level='DEBUG')],
)
ignore_logger("werkzeug")


# Logging config
class StackdriverJsonFormatter(jsonlogger.JsonFormatter):
    """
    Formatter for the Stackdriver JSON logs.
    """

    def __init__(self, fmt='%(asctime)s %(levelname)s %(message)s', style='%', *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record: dict) -> dict:
        """
        Normalization of fields so Stackdriver can understand them. More info:
        https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry

        :param log_record: Python log record object.
        :return: The transformed log record.
        """
        # Fields remapping
        log_record['app'] = log_record['name']
        log_record['timestamp'] = log_record['asctime']
        log_record['severity'] = log_record['levelname']

        # Cleaning up
        del log_record['name']
        del log_record['asctime']
        del log_record['levelname']

        return super(StackdriverJsonFormatter, self).process_log_record(log_record)


handler = logging.StreamHandler(sys.stdout)
formatter = StackdriverJsonFormatter(
    fmt='%(asctime)s %(levelname)s %(module)s %(message)s %(name)s'
)
handler.setFormatter(formatter)

app_logger = logging.getLogger('myapi')
app_logger.addHandler(handler)
app_logger.setLevel(logging.DEBUG)
