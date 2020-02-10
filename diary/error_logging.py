from pydantic import ValidationError


class DataError(RuntimeError):

    def __init__(self, value: any, pydantic_error: ValidationError):
        self.value = value
        self.validation_error = pydantic_error
