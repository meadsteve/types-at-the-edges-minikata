from scripts.common import run, handle_error

if __name__ == "__main__":
    try:
        run("the-second-day")
    except Exception as ooops:
        extra_detail = \
            "We spoke to the owners of the API and they've told us that some beta users can apply multiple categories.\n" \
            "We should index the entry against each of the categories it has.\n" \
            "Can you update the code please?"
        handle_error(ooops, extra_detail)
