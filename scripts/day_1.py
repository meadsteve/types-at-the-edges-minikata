from diary.error_logging import DataError
from diary.indexer import run_indexing


if __name__ == "__main__":
    try:
        indexed = run_indexing("the-first-day")
        print("Successfully indexed data")
        print(f"{len(indexed.entries)} entries")
        print(f"{len(indexed.title_index.keys())} unique titles")
        print(f"{len(indexed.category_index.keys())} unique categories")
    except DataError as ooops:
        print("!!!!!!")
        print("Oh dear. We looked in our error logs and saw this error today:")
        print("")
        print(str(ooops.validation_error))
        print("")
        print("We spoke to the owners of the API and they discovered that not all entries have a title.")
        print("As a team we decided these should be indexed as having an empty string for the title.")
        print("Can you update the code please?")
