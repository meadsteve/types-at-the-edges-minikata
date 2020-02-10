import random
import re
from typing import List, Dict


class Response:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


url_pattern = re.compile(r"https://(?P<server>[^/]+)/.+")


EXAMPLE_PAYLOADS: Dict[str, List] = {
    "dev": [
        {"title": "today was fun", "body": "it really was", "category": "general", "entry_ts": "2020-01-10 12:22"},
        {"title": "today was fun  ", "body": "it really was", "category": "generaL", "entry_ts": "2020-01-11 12:00"},
        {"title": "all good", "body": "bloop", "category": "General", "entry_ts": "2020-01-12 05:22"}
    ],
    "the-first-day": [
        {"title": "today was fun", "body": "it really was", "category": "general", "entry_ts": "2020-01-04 12:22"},
        {"title": "today was fun  ", "body": "it really was", "category": "generaL", "entry_ts": "2020-01-09 12:22"},
        {"title": "all good", "body": "bloop", "category": "General", "entry_ts": "2020-01-13 12:22"},
        {"title": None, "body": "I'm typing what I'm thinking. I don't know what this is or where it'll go", "category": "Stream of consciousness", "entry_ts": "2019-01-09 12:22"}
    ]
}


def get(path):
    url_parts = url_pattern.match(path)
    if not url_parts:
        raise Exception(f"cannot connect to: {path}")
    server = url_parts.group('server')
    if server not in EXAMPLE_PAYLOADS:
        raise Exception(f"cannot connect to: {path}")
    choices = EXAMPLE_PAYLOADS[server]
    if not choices:
        raise Exception("No data loaded for this server")
    return Response(random.choice(choices))
