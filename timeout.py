"""Module providing a timeout (single threaded) functionality in form of decorator."""

import errno
import os
import signal
import functools
import time

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    """
    Decorator function that adds a timeout to the decorated function.

    Args:
        seconds (int, optional): The number of seconds after which the function should timeout. Defaults to 10.
        error_message (str, optional): The error message to raise if the function times out. Defaults to the system-specific error message for ETIME.

    Returns:
        function: The decorated function with a timeout added.

    Raises:
        TimeoutError: If the function times out before completing.

    Example:
        @timeout(5)
        def long_running_function():
            time.sleep(10)

        try:
            long_running_function()
        except TimeoutError:
            print("Function timed out")
    """
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator

@timeout(seconds=3)
def long_running_function():
    time.sleep(2)

long_running_function()
