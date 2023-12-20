#!/usr/bin/env python3

import requests
import redis
from functools import wraps
from time import time

# Connect to Redis server
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def cache_with_expiration(expiration_time):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            cache_key = f"count:{url}"
            cached_result = redis_client.get(cache_key)

            if cached_result:
                return cached_result.decode('utf-8')

            result = func(*args, **kwargs)

            # Cache the result with expiration time
            redis_client.setex(cache_key, expiration_time, result)

            return result

        return wrapper
    return decorator

@cache_with_expiration(expiration_time=10)
def get_page(url):
    response = requests.get(url)
    return response.text

# Example usage
if __name__ == "__main__":
    slow_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"

    # First request, uncached
    page_content = get_page(slow_url)
    print("First request:", page_content)

    # Second request, cached
    page_content = get_page(slow_url)
    print("Second request:", page_content)
