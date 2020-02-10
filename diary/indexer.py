from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List

from pydantic import ValidationError
from pydantic.main import BaseModel

from fakes import requests
from .error_logging import DataError


class DiaryEntry(BaseModel):
    title: str
    body: str
    category: str
    entry_ts: datetime


CategoryIndex = Dict[str, List[DiaryEntry]]
TitleIndex = Dict[str, List[DiaryEntry]]


@dataclass
class IndexedData:
    entries: List[DiaryEntry]
    category_index: CategoryIndex
    title_index: TitleIndex


class MyApiClient:
    def __init__(self, server: str):
        self.server = server

    def fetch_entry(self, id: int) -> DiaryEntry:
        payload = requests.get(f"https://{self.server}/journal/entry/{id}")
        json = payload.json()
        try:
            return DiaryEntry(**json)
        except ValidationError as validation_failure:
            raise DataError(json, validation_failure)


def run_indexing(server: str):
    category_index: CategoryIndex = defaultdict(list)
    title_index: TitleIndex = defaultdict(list)
    entries: List[DiaryEntry] = []

    client = MyApiClient(server)
    for entry_id in range(0, 1000):
        new_entry = client.fetch_entry(entry_id)

        entries.append(new_entry)
        add_to_category_index(category_index, new_entry)
        add_to_title_index(title_index, new_entry)

    entries.sort(key=diary_entry_date)

    return IndexedData(entries, category_index, title_index)


def add_to_title_index(title_index: TitleIndex, new_entry: DiaryEntry):
    title_index[new_entry.title.strip()].append(new_entry)


def add_to_category_index(category_index: CategoryIndex, new_entry: DiaryEntry):
    category_index[new_entry.category.lower()].append(new_entry)


def diary_entry_date(entry: DiaryEntry) -> date:
    return entry.entry_ts.date()
