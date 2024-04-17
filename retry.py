from random import random
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
                        raise Exception('Failed all attempts to exec logic') from e
                else:
                    return result
        return inner_function
    return wrapper


@retry(tries=5, pause=0.1)
def foo(val: int) -> int:
    """
    Retry decorator demo function.

    This function will be tried to execute number of times equal to `tries`
    In case of exception it will wait for `pause` seconds and try again
    If all attempts failed decorator will raise exception from the last attempt

    :param val: input integer value
    :return: the same input value if function called successfully
    """
    if random() < 0.5:
        raise Exception('Bad luck')
    return val



for index in range(10):
    print(foo(index))
