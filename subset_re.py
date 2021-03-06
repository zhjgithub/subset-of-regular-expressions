'''
Exercise of subset of Regular Expressions implement.
'''

from decorator import decorator

null = frozenset()
dot = lambda text: set([text[1:]]) if text else null
eol = lambda text: set(['']) if text == '' else null


def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m is not None:
            return m


def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    remainders = pattern(text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text) - len(shortest)]


def lit(s):
    return lambda text: set([text[len(s):]]) if text.startswith(s) else null


def seq(x, y):
    return lambda text: set.union(*map(y, x(text)))


def alt(x, y):
    return lambda text: set.union(x(text), y(text))


def star(x):
    return lambda text: set([text]) | set(t2 for t1 in x(text) if t1 != text for t2 in star(x)(t1))


def plus(x):
    return seq(x, star(x))


def opt(x):
    return alt(lit(''), x)  #opt(x) means that x is optional


def oneof(chars):
    return lambda text: set([text[1:]]) if text and text[0] in chars else null


@decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""

    def n_ary_f(x, *args):
        # if not args:
        #     return x
        # elif len(args) == 1:
        #     return f(x, *args)
        # return f(x, n_ary_f(args[0], *args[1:]))
        return x if not args else f(x, n_ary_f(*args))

    return n_ary_f


def matchset(pattern, text):
    '''
    Match pattern at start of text; return a set of remainders of text.
    '''
    op, x, y = components(pattern)
    if op == 'lit':
        return set([text[len(x):]]) if text.startswith(x) else null
    elif op == 'seq':
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif op == 'alt':
        return matchset(x, text) | matchset(y, text)
    elif op == 'dot':
        return set([text[1:]]) if text else null
    elif op == 'oneof':
        return set([text[1:]]) if text.startswith(x) else null
    elif op == 'eol':
        return set(['']) if text == '' else null
    elif op == 'star':
        return (set([text]) | set(
            t2 for t1 in matchset(x, text) for t2 in matchset(pattern, t1)
            if t1 != text))
    else:
        raise ValueError('unknown pattern: {}'.format(pattern))


def components(pattern):
    "Return the op, x, and y arguments; x and y are None if missing."
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    return pattern[0], x, y


def test():
    "Tests."
    assert lit('abc') == ('lit', 'abc')
    assert seq(('lit', 'a'), ('lit', 'b')) == ('seq', ('lit', 'a'), ('lit',
                                                                     'b'))
    assert alt(('lit', 'a'), ('lit', 'b')) == ('alt', ('lit', 'a'), ('lit',
                                                                     'b'))
    assert star(('lit', 'a')) == ('star', ('lit', 'a'))
    assert plus(('lit', 'c')) == ('seq', ('lit', 'c'), ('star', ('lit', 'c')))
    assert opt(('lit', 'x')) == ('alt', ('lit', ''), ('lit', 'x'))
    assert oneof('abc') == ('oneof', ('a', 'b', 'c'))

    assert matchset(('lit', 'abc'), 'abcdef') == set(['def'])
    assert matchset(('seq', ('lit', 'hi '), ('lit', 'there ')),
                    'hi there nice to meet you') == set(['nice to meet you'])
    assert matchset(('alt', ('lit', 'dog'), ('lit', 'cat')),
                    'dog and cat') == set([' and cat'])
    assert matchset(('dot', ), 'am i missing something?') == set(
        ['m i missing something?'])
    assert matchset(oneof('a'), 'aabc123') == set(['abc123'])
    assert matchset(oneof('ab'), 'aabc123') == set(['abc123'])
    assert matchset(('eol', ), '') == set([''])
    assert matchset(('eol', ), 'not end of line') == frozenset([])
    assert matchset(('star', ('lit', 'hey')),
                    'heyhey!') == set(['!', 'heyhey!', 'hey!'])

    assert match(('star', ('lit', 'a')), 'aaabcd') == 'aaa'
    assert match(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') is None
    assert match(('alt', ('lit', 'b'), ('lit', 'a')), 'ab') == 'a'
    assert search(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == 'b'

    g = alt(lit('a'), lit('b'))
    assert g('abc') == set(['bc'])

    return 'tests pass'


def test2():
    def f(x, y):
        return x + y

    fn = n_ary(f)

    print(fn(1))
    print(fn(1, 2))
    print(fn(1, 2, 3))
    print(fn(1, 2, 3, 4))

    def test_fun(x, y):
        return ('seq', x, y)

    test_fun = n_ary(test_fun)
    print(test_fun(1, 2, 3, 4))

    @n_ary
    def test_fun2(x, y):
        "test_fun2 wrapped in decorator"
        return ('seq', x, y)

    print(test_fun2(1, 2, 3, 4))
    help(test_fun2)
    help(n_ary)
    print('test2 success')


if __name__ == '__main__':
    # print(test())
    test2()
