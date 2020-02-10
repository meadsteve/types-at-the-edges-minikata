from collections import defaultdict

from diary.indexer import add_to_title_index, DiaryEntry, add_to_category_index, TitleIndex, CategoryIndex


def test_titles_have_white_space_stripped():
    entry = DiaryEntry(title=" hello   ", body="", categories=["general"], entry_ts="2020-01-09 12:22")
    index: TitleIndex = defaultdict(list)
    add_to_title_index(index, entry)

    assert len(index[" hello   "]) == 0
    assert len(index["hello"]) == 1


def test_categories_are_lower_cased():
    entry = DiaryEntry(title="hello", body="", categories=["GENERAL"], entry_ts="2020-01-09 12:22")
    index: CategoryIndex = defaultdict(list)
    add_to_category_index(index, entry)

    assert len(index["GENERAL"]) == 0
    assert len(index["general"]) == 1
