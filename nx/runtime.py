class ExternalDecorator:

    def __init__(self, func):
        self._func = func

    def __call__(self):
        self._func()


external = ExternalDecorator


@external
class Reference:
    ...
