def get(func):
    def wrapper_func(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper_func
