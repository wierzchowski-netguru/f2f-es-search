import functools

from django.db import connection
from django.utils import timezone


def request_stats(func):
    """
    Decorator to check request time, queries, for dev purposes.
    """
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        calls_before = len(connection.queries)
        time_before = timezone.now()

        value = func(*args, **kwargs)

        calls_after = len(connection.queries)
        time_after = timezone.now()

        for query in connection.queries[calls_before:calls_after]:
            print(f'>>> {query["sql"]}')
            print(f'>>> {query["time"]}')

        print(f'>>> Request time: {time_after - time_before}')
        print(f'>>> Request db connections: {calls_after - calls_before}')

        return value

    return wrapper_decorator
