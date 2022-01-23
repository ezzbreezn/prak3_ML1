from functools import wraps


def check_arguments(*arg_types):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(arg_types) > len(args):
                raise TypeError
            for arg_type, arg in zip(arg_types, args):
                if not isinstance(arg, arg_type):
                    raise TypeError
            return func(*args, **kwargs)
        return wrapper
    return decorator
