from functools import wraps

def RetryDecorator(retries: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwags):
            for _ in range(retries):
                try:
                    func_result = func(*args, **kwags)
                except Exception as e:
                    continue
                return func_result
        return wrapper
    return decorator