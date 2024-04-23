"""Module providing a call limiting functionality in form of decorator."""

import time
from collections import deque
from functools import wraps

def limit_calls(number_of_calls: int=10, control_period: int=1):
    """
    A decorator function that limits the number of function calls per second.

    Parameters:
        number_of_calls (int): The maximum number of function calls allowed within the control period. Default is 10.
        control_period (int): The time period in seconds for which the number of function calls is controlled. Default is 1.

    Returns:
        function: The decorated function.

    Example:
        @limit_calls(number_of_calls=5, control_period=2)
        def my_function():
            # function code here

        my_function()  # calls the function with limited calls per second
    """
    queue = deque(maxlen=number_of_calls)

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_time = time.time()

            if len(queue) == number_of_calls and current_time - queue[0] < control_period:
                print('Skip function call')

                return None

            result = func(*args, **kwargs)
            queue.append(current_time)

            return result
        return inner

    return wrapper
