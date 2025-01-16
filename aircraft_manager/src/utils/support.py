# Third party imports
import time


def elapsed_time(func):
    def wrapper():
        start_time: float = time.time()

        func()

        end_time: float = time.time() - start_time
        print(f"{func.__name__.capitalize()} took {end_time} s.")

    return wrapper
