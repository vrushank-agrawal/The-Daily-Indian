# Create an exception class for handling errors

class APIError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message



