from scripts.common import run, handle_error

if __name__ == "__main__":
    try:
        run("the-third-day")
    except Exception as ooops:
        extra_detail = \
            "We spoke to the owners of the API and they've told us that users can save 'in draft' entries.\n" \
            "We don't need to index these at all. Let's filter them out\n" \
            "Can you update the code please?"
        handle_error(ooops, extra_detail)
