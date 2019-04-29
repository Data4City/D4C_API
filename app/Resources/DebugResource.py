from models import __reset_db__


class DebugResource:
    def on_get(self, req, res):
        __reset_db__()
        res.json({"ok": "Database reset"})