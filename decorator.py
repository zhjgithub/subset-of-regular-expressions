'''
Decorator and update_wrapper.
'''

from functools import update_wrapper


def decorator(d):
    "Make function d a decorator: d wrap a function fn."

    def _d(fn):
        return update_wrapper(d(fn), fn)

    update_wrapper(_d, d)
    return _d


@decorator
def memo(f):
    '''
    Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up.
    '''
    cache = {}

    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(*args)

    return _f


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@memo
def fibonacci_with_cache(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def decorator2(d):
    "make function d a decorator2, return lamda"
    return lambda fn: update_wrapper(d(fn), fn)


decorator2 = decorator2(decorator2)


def test():
    import time
    start = time.clock()
    print(fibonacci(20))
    print(time.clock() - start)
    start = time.clock()
    print(fibonacci_with_cache(20))
    print(time.clock() - start)
    start = time.clock()
    print(fibonacci_with_cache(20))
    print(time.clock() - start)
    print('test success')


if __name__ == '__main__':
    test()