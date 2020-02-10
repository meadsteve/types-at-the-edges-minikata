from collections import defaultdict
from datetime import datetime

from diary.indexer import add_to_title_index, RawEntry, add_to_category_index, TitleIndex, CategoryIndex, PublishedEntry


def test_titles_have_white_space_stripped():
    entry = PublishedEntry(title=" hello   ", body="", categories=["general"], entry_ts=datetime.now())
    index: TitleIndex = defaultdict(list)
    add_to_title_index(index, entry)

    assert len(index[" hello   "]) == 0
    assert len(index["hello"]) == 1


def test_categories_are_lower_cased():
    entry = PublishedEntry(title="hello", body="", categories=["GENERAL"], entry_ts=datetime.now())
    index: CategoryIndex = defaultdict(list)
    add_to_category_index(index, entry)

    assert len(index["GENERAL"]) == 0
    assert len(index["general"]) == 1
