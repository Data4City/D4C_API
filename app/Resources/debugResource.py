from Scripts.OpenSenseMapCrawler import crawl_results
from models import __reset_db__


class DebugResource:
    def on_post(self, req, resp):
        __reset_db__()
        resp.body = "Reset"

    def on_put(self, req, resp):
        crawl_results()
