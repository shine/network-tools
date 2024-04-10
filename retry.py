from random import random
from functools import wraps
import time


def retry(tries: int, pause: float):
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
def foo(val: int):
    if random() < 0.5:
        raise Exception('Bad luck')
    return val



for index in range(10):
    print(foo(index))
