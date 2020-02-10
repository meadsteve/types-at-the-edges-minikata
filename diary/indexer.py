from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List, Optional, Union

from pydantic import ValidationError
from pydantic.main import BaseModel
from typing_extensions import Literal

from fakes import requests
from .error_logging import DataError


class RawEntry(BaseModel):
    title: Optional[str]
    body: str
    category: Union[str, List[str]]
    entry_ts: Union[datetime, Literal["PENDING"]]


@dataclass
class PublishedEntry:
    title: str
    body: str
    categories: List[str]
    entry_ts: datetime


CategoryIndex = Dict[str, List[PublishedEntry]]
TitleIndex = Dict[str, List[PublishedEntry]]


@dataclass
class IndexedData:
    entries: List[PublishedEntry]
    category_index: CategoryIndex
    title_index: TitleIndex


class MyApiClient:
    def __init__(self, server: str):
        self.server = server

    def fetch_entry(self, id: int) -> RawEntry:
        payload = requests.get(f"https://{self.server}/journal/entry/{id}")
        json = payload.json()
        try:
            return RawEntry(**json)
        except ValidationError as validation_failure:
            raise DataError(json, validation_failure)


def run_indexing(server: str):
    category_index: CategoryIndex = defaultdict(list)
    title_index: TitleIndex = defaultdict(list)

    client = MyApiClient(server)
    all_entries = (client.fetch_entry(id) for id in range(0, 1000))

    # All of the quirks in the raw api get normalised
    # in the published_entry function. The pending entries
    # are skipped as we didn't want these
    published_entries: List[PublishedEntry] = [
        published_entry(raw) for raw in all_entries if raw.entry_ts != "PENDING"
    ]

    for entry in published_entries:
        add_to_category_index(category_index, entry)
        add_to_title_index(title_index, entry)

    published_entries.sort(key=diary_entry_date)

    return IndexedData(published_entries, category_index, title_index)


def add_to_title_index(title_index: TitleIndex, new_entry: PublishedEntry):
    title_index[new_entry.title.strip()].append(new_entry)


def add_to_category_index(category_index: CategoryIndex, new_entry: PublishedEntry):
    for category in new_entry.categories:
        category_index[category.lower()].append(new_entry)


def diary_entry_date(entry: PublishedEntry) -> date:
    return entry.entry_ts.date()


def published_entry(raw: RawEntry) -> PublishedEntry:
    if not isinstance(raw.entry_ts, datetime):
        raise RuntimeError("entry_ts was not a valid datetime")
    return PublishedEntry(
        title=raw.title or "",
        body=raw.body,
        categories=raw.category if isinstance(raw.category, list) else [raw.category],
        entry_ts=raw.entry_ts
    )
