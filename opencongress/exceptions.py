class NoApiKeyProvided(BaseException):
    def __str__(self):
        return 'No API key provided'


class HTTPError(IOError):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return 'Response code %s returned' % self.code


class ArgumentError(RuntimeError):
    pass