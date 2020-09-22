from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List, Optional, Union, Protocol, Literal

from pydantic import ValidationError
from pydantic.main import BaseModel

from fakes import requests
from .error_logging import DataError


class RawDiaryEntry(BaseModel):
    title: Optional[str]
    body: str
    category: Union[str, List[str]]
    entry_ts: Union[datetime, Literal["PENDING"]]


class DiaryEntry(BaseModel):
    title: str
    body: str
    categories: List[str]
    entry_ts: datetime

    @classmethod
    def from_raw(cls, raw):
        categories = [raw.category] if isinstance(raw.category, str) else raw.category
        title = raw.title or ""
        if raw.entry_ts == "PENDING":
            raise RuntimeError("Expected a saved entry. Not a pending one")
        return cls(categories=categories, title=title, body=raw.body, entry_ts=raw.entry_ts)


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

    def fetch_entry(self, id: int) -> RawDiaryEntry:
        payload = requests.get(f"https://{self.server}/journal/entry/{id}")
        json = payload.json()
        try:
            return RawDiaryEntry(**json)
        except ValidationError as validation_failure:
            raise DataError(json, validation_failure) from validation_failure


def run_indexing(server: str):
    category_index: CategoryIndex = defaultdict(list)
    title_index: TitleIndex = defaultdict(list)
    entries: List[DiaryEntry] = []

    client = MyApiClient(server)
    for entry_id in range(0, 1000):
        raw_entry = client.fetch_entry(entry_id)
        if raw_entry.entry_ts != "PENDING":
            entry = DiaryEntry.from_raw(raw_entry)
            entries.append(entry)
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
