'''
Decorator and update_wrapper.
'''

from functools import update_wrapper


def disabled(f):
    "Disable a decorator, like some_decorator = disabled."
    return f


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


callcounts = {}


@decorator
def countcalls(f):
    "Decorator that makes the function count calls to it, in callcounts[f]"

    def _f(*args):
        callcounts[_f] += 1
        return f(*args)

    callcounts[_f] = 0
    return _f


@decorator
def trace(f):
    indent = '   '

    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print('%s--> %s' % (trace.level * indent, signature))
        trace.level += 1
        try:
            result = f(*args)
            print('%s<-- %s == %s' % ((trace.level - 1) * indent, signature,
                                      result))
        finally:
            trace.level -= 1
        return result

    trace.level = 0
    return _f


trace = disabled


@trace
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@trace
@memo
@countcalls
def fibonacci_with_cache(n):
    if n <= 1:
        return n
    return fibonacci_with_cache(n - 1) + fibonacci_with_cache(n - 2)


def decorator2(d):
    "make function d a decorator2, return lambda"
    return lambda fn: update_wrapper(d(fn), fn)


decorator2 = decorator2(decorator2)


def test():
    import time
    start = time.clock()
    print(fibonacci(6))
    print(time.clock() - start)
    start = time.clock()
    print(fibonacci_with_cache(20))
    print(time.clock() - start)
    start = time.clock()
    print(fibonacci_with_cache(20))
    print(time.clock() - start)
    print(callcounts)
    print('test success')


if __name__ == '__main__':
    test()
