from datetime import datetime
import random
from functools import lru_cache


def external_api():
    return round(random.uniform(10.0, 100.0), 2)


def get_cache_key():
    return datetime.now().date()


@lru_cache(maxsize=1)
def get_cached_calculation(day: datetime.date):
    """Cached function that fetches the calculation once per day."""
    return external_api()