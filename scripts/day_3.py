from diary.error_logging import DataError
from diary.indexer import run_indexing


if __name__ == "__main__":
    try:
        indexed = run_indexing("the-third-day")
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
        print("The raw data for the entry was")
        print(str(ooops.value))
        print("")
        print("We spoke to the owners of the API and they've told us that users can save 'in draft' entries.")
        print("We don't need to index these at all. Let's filter them out")
        print("Can you update the code please?")
