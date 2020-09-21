from diary.error_logging import DataError
from diary.indexer import run_indexing


def run(server_name):
    indexed = run_indexing(server_name)
    print("Successfully indexed data")
    print(f"{len(indexed.entries)} entries")
    print(f"{len(indexed.title_index.keys())} unique titles")
    print(f"{len(indexed.category_index.keys())} unique categories")


def handle_error(error: Exception, extra_text):
    print("!!!!!!")
    print("Oh dear. We looked in our error logs and saw this error today:")
    print("")
    if isinstance(error, DataError):
        print(str(error.validation_error))
        print("")
        print("The raw data for the entry was")
        print(str(error.value))
    else:
        print(str(error))
    print("")
    print(extra_text)