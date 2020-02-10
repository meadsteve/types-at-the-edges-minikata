from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List, Optional

from pydantic import ValidationError
from pydantic.main import BaseModel

from fakes import requests
from .error_logging import DataError


class DiaryEntry(BaseModel):
    title: str
    body: str
    categories: List[str]
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

    def fetch_entry(self, id: int) -> Optional[DiaryEntry]:
        payload = requests.get(f"https://{self.server}/journal/entry/{id}")
        json = payload.json()
        try:
            if json["entry_ts"] == "PENDING":
                return None
            if not json["title"]:
                json["title"] = ""
            json["categories"] = json["category"] if isinstance(json["category"], list) else [json["category"]]
            return DiaryEntry(**json)
        except ValidationError as validation_failure:
            raise DataError(json, validation_failure)


def run_indexing(server: str):
    category_index: CategoryIndex = defaultdict(list)
    title_index: TitleIndex = defaultdict(list)

    client = MyApiClient(server)
    all_entries = (client.fetch_entry(entry_id) for entry_id in range(0, 1000))
    entries = [entry for entry in all_entries if entry is not None]
    for entry in entries:
        add_to_category_index(category_index, entry)
        add_to_title_index(title_index, entry)

    entries.sort(key=diary_entry_date)

    return IndexedData(entries, category_index, title_index)


def add_to_title_index(title_index: TitleIndex, new_entry: DiaryEntry):
    title_index[new_entry.title.strip()].append(new_entry)


def add_to_category_index(category_index: CategoryIndex, new_entry: DiaryEntry):
    for category in new_entry.categories:
        category_index[category.lower()].append(new_entry)


def diary_entry_date(entry: DiaryEntry) -> date:
    return entry.entry_ts.date()
