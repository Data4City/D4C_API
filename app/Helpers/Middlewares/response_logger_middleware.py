import falcon
import logging


class ResponseLoggerMiddleware:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_request(self, req, resp):
        self.logger.info('{0} {1} {2}'.format(req.method, req.relative_uri, resp.status[:3]))
