import logging
from datetime import datetime


class ResponseLoggerMiddleware:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging started")

    def process_response(self, req, resp, resource, req_succeeded):
        delta = datetime.now() - req.context["start_time"]
        self.logger.info('{0} | {1} | {2} | {3} | {4} ms'.format(req.method, req.relative_uri, resp.status, req.json, delta.microseconds / 1000))

    def process_request(self, req, resp):
        req.context["start_time"] = datetime.now()
