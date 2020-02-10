from diary.indexer import run_indexing

if __name__ == "__main__":
    indexed = run_indexing("dev")
    print("Successfully indexed data")
    print(f"{len(indexed.entries)} entries")
    print(f"{len(indexed.title_index.keys())} unique titles")
    print(f"{len(indexed.category_index.keys())} unique categories")
