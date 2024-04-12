"""Module providing a circuit breaker functionality in form of decorator."""

import time
from functools import wraps
from random import random
from collections import deque


def circuit_breaker(history_size: int=5, forget_after: int=3):
    """
        Circuit breaker decorator. It remembers results of previous function calls and 
        prevents following call in case of malfunctioning.

        history_size: number of previous function call to remember and to make call/skip decision.
        forget_after: seconds to keep remembered call result.
    """
    queue = deque(maxlen=history_size)

    def call_probability() -> float:
        empty_items_in_queue = history_size - len(queue)
        success_items_in_queue = sum(item['status'] for item in queue)

        return (success_items_in_queue + empty_items_in_queue)/history_size

    def clean_outdated_history(current_time) -> None:
        if queue:
            while current_time - queue[0]['timestamp'] > forget_after:
                queue.popleft()

    def remember_call(current_time, success=True):
        new_status_value = 1 if success else 0

        queue.append({'timestamp': current_time, 'status': new_status_value})

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


@circuit_breaker()
def random_exception(val: int, probability: float):
    """ Just a method that fails randomely """
    if random() < probability:
        raise ValueError('Bad luck')
    return val


for index in range(30):
    print(random_exception(index, 0.9))
    time.sleep(0.3)

print('Functionality was fixed!')

for index in range(30):
    print(random_exception(index, 0.05))
    time.sleep(0.3)
