'''
Exercise of subset of Regular Expressions implement.
'''

null = frozenset()
dot = ('dot', )
eol = ('eol', )


def lit(string):
    return ('lit', string)


def seq(x, y):
    return ('seq', x, y)


def alt(x, y):
    return ('alt', x, y)


def star(x):
    return ('star', x)


def plus(x):
    return (seq(x, star(x)))


def opt(x):
    return alt(lit(''), x)  #opt(x) means that x is optional


def oneof(chars):
    return ('oneof', tuple(chars))


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
        return set([text[1:]]) if any(text.startswith(i) for i in x) else null
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
    assert matchset(('oneof', 'a'), 'aabc123') == set(['abc123'])
    assert matchset(('oneof', 'ab'), 'aabc123') == set(['abc123'])
    assert matchset(('eol', ), '') == set([''])
    assert matchset(('eol', ), 'not end of line') == frozenset([])
    assert matchset(('star', ('lit', 'hey')),
                    'heyhey!') == set(['!', 'heyhey!', 'hey!'])

    return 'tests pass'


if __name__ == '__main__':
    print(test())
