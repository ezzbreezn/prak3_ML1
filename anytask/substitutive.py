from functools import wraps
from inspect import signature


def substitutive(func, fix_args=None):
    if fix_args is None:
        fix_args = ()

    @wraps(func)
    def wrapper(*args, **kwargs):
        full_args = fix_args + args
        if len(signature(func).parameters) == len(full_args):
            return func(*full_args)
        elif len(signature(func).parameters) > len(full_args):
            return substitutive(func, full_args)
        else:
            raise TypeError
    return wrapper
