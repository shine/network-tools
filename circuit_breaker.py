"""Module providing a circuit breaker functionality in form of decorator."""

import time
from functools import wraps
from random import random
from collections import deque


def circuit_breaker(history_size: int=5, forget_after: int=3):
    """
    Circuit breaker decorator. It remembers results of previous function calls and 
    prevents following call in case of malfunctioning.

    Parameters:
        history_size (int): number of previous function call to remember and
                            to make call/skip decision. Default is 5.
        forget_after (int): seconds to keep remembered call results. Default is 3.

    Returns:
        function: the decorated function

    Example:
        @circuit_breaker(history_size=3, forget_after=2)
        def my_function():
            # function code here

        my_function()  # calls the function with circuit breaker functionality
    """
    queue = deque(maxlen=history_size)

    def call_probability() -> float:
        total_items = sum(item['status'] for item in queue) + (history_size - len(queue))

        return total_items / history_size

    def clean_outdated_history(current_time):
        while queue and current_time - queue[0]['timestamp'] > forget_after:
            queue.popleft()

    def remember_call(timestamp, success=True):
        queue.append({'timestamp': timestamp, 'status': int(success)})

    def wrapper(func):
        @wraps(func)
        def inner_function(*args, **kwargs):
            result = None
            current_time = time.time()

            clean_outdated_history(current_time)

            try:
                if random() < call_probability():
                    result = func(*args, **kwargs)

                    remember_call(current_time)
                else:
                    print('Skip function call')
            except Exception:
                remember_call(current_time, False)

            return result

        return inner_function
    return wrapper
