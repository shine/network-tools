import time
from collections import deque
from functools import wraps

def limit_calls(number_of_calls: int=10, control_period: int=1):
    """
        control_period (int): period of time in seconds we control number of calls over
        number_of_calls (int): maximum allowed number of calls during control period
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

@limit_calls(number_of_calls=3, control_period=1)
def request_something_from_api(url, timeout):
    print(f'Call: {url} and {timeout}')

for _ in range(5):
    request_something_from_api('https://google.com', 20)

time.sleep(1)

for _ in range(5):
    request_something_from_api('https://bing.com', 10)
