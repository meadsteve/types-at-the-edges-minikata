from diary.error_logging import DataError
from diary.indexer import run_indexing


if __name__ == "__main__":
    try:
        indexed = run_indexing("the-second-day")
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
        print("We spoke to the owners of the API and they've told us that some beta users can apply multiple categories.")
        print("We should index the entry against each of the categories it has.")
        print("Can you update the code please?")
