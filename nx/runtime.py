class ExternalDecorator:
    """ Defines external references """

    def __init__(self, func):
        self._func = func

    def __call__(self):
        self._func()


external = ExternalDecorator


@external
class Reference:
    ...


class EntrypointDecorator:
    """ Defines exports """
    exports: list = []

    def __init__(self, func):
        self._func = func
        self.exports.append(func)
        print('IT WORKS!')

    def __call__(self):
        self._func()


entrypoint = EntrypointDecorator
