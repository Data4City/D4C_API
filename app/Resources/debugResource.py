from Scripts.OpenSenseMapCrawler import crawl_results
from Models import reset_db


class DebugResource:
    def on_post(self, req, resp):
        reset_db()
        resp.body = "Reset"

    def on_put(self, req, resp):
        crawl_results()
