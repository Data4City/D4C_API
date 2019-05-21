import logging
import falcon


class ResponseLoggerMiddleware:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging started")

    def process_request(self, req, resp):
        self.logger.info('{0} {1} {2} {3}'.format(req.method, req.relative_uri, resp.status, req.json))
