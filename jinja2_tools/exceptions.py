from colors import red


class InvalidDataType(Exception):
    def __init__(self, message=f"{red('[ERROR]')} Invalid data type, try '-' for stdin, valid URL or path on your file system."):
        self.message = message
        super().__init__(self.message)


class InvalidInput(Exception):
    def __init__(self, message=f"{red('[ERROR]')} Invalid input, stdin can be used for data or template but not both."):
        self.message = message
        super().__init__(self.message)
