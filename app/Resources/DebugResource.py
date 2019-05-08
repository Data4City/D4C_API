from Helpers.helper_functions import create_db_connection_url
from models import __reset_db__


class DebugResource:
    def on_post(self, req, resp):
        print(create_db_connection_url())
        __reset_db__()
        # resp.json({"ok": "Database reset"})
