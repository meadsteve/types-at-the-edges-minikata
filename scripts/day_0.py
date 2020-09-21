from scripts.common import handle_error, run

if __name__ == "__main__":
    try:
        run("dev")
    except Exception as error:
        handle_error(error, "Erm... We didn't really expect it to fail in dev")
