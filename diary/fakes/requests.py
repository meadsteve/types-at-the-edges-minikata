import random
import re


class Response:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


url_pattern = re.compile(r"https://(?P<server>[^/]+)/.+")


EXAMPLE_PAYLOADS = {
    "dev": [
        {"title": "today was fun", "body": "it really was", "category": "general", "entry_ts": "2020-01-09 12:22"},
        {"title": "today was fun  ", "body": "it really was", "category": "generaL", "entry_ts": "2020-01-09 12:22"},
        {"title": "all good", "body": "bloop", "category": "General", "entry_ts": "2020-01-09 12:22"}
    ]
}


def get(path):
    url_parts = url_pattern.match(path)
    if not url_parts:
        raise Exception(f"cannot connect to: {path}")
    server = url_parts.group('server')
    if server not in EXAMPLE_PAYLOADS:
        raise Exception(f"cannot connect to: {path}")
    return Response(random.choice(EXAMPLE_PAYLOADS[server]))
