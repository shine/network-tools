"""Module providing a function call retry functionality in form of decorator."""

from functools import wraps
import time


def retry(tries: int = 5, pause: float = 1.5):
    """
    Retry decorator.

    Decorated function will be tried to execute number of times equal to `tries`
    In case of exception it will wait for `pause` seconds and try again
    If all attempts failed decorator will raise exception from the last attempt

    :param tries: number of attempts to execute decorated function
    :param pause: seconds to wait before next retry
    :return: decorated function
    """
    def wrapper(func):
        @wraps(func)
        def inner_function(*args, **kwargs):
            for attempt in range(tries):
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    if attempt < tries-1:
                        print('Exception happened. Lets try again')
                        time.sleep(pause)
                    else:
                        raise RuntimeError('Failed all attempts to exec logic') from e
                else:
                    return result
        return inner_function
    return wrapper
