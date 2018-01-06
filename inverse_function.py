'''
Inverse function.
'''


def slow_inverse(f, delta=1 / 1024):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""

    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x) - y < y - f(x - delta)) else x - delta

    return f_1


def inverse(f, delta=1 / 1024):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""

    def f_1(y):
        lo, hi = found_bounds(f, y)
        return binary_search(f, y, lo, hi, delta)

    return f_1


def found_bounds(f, y):
    '''
    Find values lo, hi such that f(lo) <= y <= f(hi).
    '''
    # Keep doubling x until f(x) >= y; that is hi;
    # and lo will be either the previous x or 0.
    x = 1
    while f(x) < y:
        x *= 2
    lo = 0 if x == 1 else x / 2
    return lo, x


def binary_search(f, y, lo, hi, delta):
    '''
    Given f(lo) <= y <= f(hi), return x such that f(x) is within delta of y.
    '''
    # Continually split the region in half
    while lo <= hi:
        x = (lo + hi) / 2
        temp = f(x)
        if temp < y:
            lo = x + delta
        elif temp > y:
            hi = x - delta
        else:
            return x
    return hi if f(hi) - y < y - f(lo) else lo


def binary_search2(f, y, lo, hi, delta):
    '''
    This version not return 0, when y is zero
    '''
    x = (lo + hi) / 2
    temp = f(x)
    while not abs(temp - y) < delta:
        if temp < y:
            lo = x
        elif temp > y:
            hi = x
        x = (lo + hi) / 2
        temp = f(x)
    return x


def test():
    "tests."

    def square(x):
        return x * x

    def power10(x):
        return 10**x

    sqrt = inverse(square)
    log10 = inverse(power10)

    print(sqrt(0))
    print(sqrt(100000000))
    print(sqrt(1000000000))
    print(log10(100000))
    print('test complete.')


if __name__ == '__main__':
    test()
