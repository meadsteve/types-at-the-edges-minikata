from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from pydantic.main import BaseModel

from fakes import requests


class DiaryEntry(BaseModel):
    title: str
    body: str
    category: str
    entry_ts: datetime


@dataclass
class IndexedData:
    entries: List[DiaryEntry]
    category_index: Dict[str, List[DiaryEntry]]
    title_index: Dict[str, List[DiaryEntry]]


class MyApiClient:
    def __init__(self, server: str):
        self.server = server

    def fetch_entry(self, id: int) -> DiaryEntry:
        payload = requests.get(f"https://{self.server}/journal/entry/{id}")
        return DiaryEntry(**payload.json())


def run_indexing(server: str):
    category_index = defaultdict(list)
    title_index = defaultdict(list)
    entries = []

    client = MyApiClient(server)
    for entry_id in range(0, 1000):
        new_entry = client.fetch_entry(entry_id)

        entries.append(new_entry)
        category_index[new_entry.category.lower()].append(new_entry)
        title_index[new_entry.title.strip()].append(new_entry)

    entries.sort(key=lambda i: i.entry_ts)

    return IndexedData(entries, category_index, title_index)
