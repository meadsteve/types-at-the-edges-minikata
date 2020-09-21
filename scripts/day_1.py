from scripts.common import run, handle_error

if __name__ == "__main__":
    try:
        run("the-first-day")
    except Exception as ooops:
        extra_detail = \
            "We spoke to the owners of the API and they discovered that not all entries have a title.\n" \
            "As a team we decided these should be indexed as having an empty string for the title.\n" \
            "Can you update the code please?"
        handle_error(ooops, extra_detail)
