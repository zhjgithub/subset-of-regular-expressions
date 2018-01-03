null = frozenset()
dot = oneof('?')
epsilon = lit('')


def lit(s):
    set_s = set([s])
    len_s = len(s)
    return lambda Ns: set_s if len_s in Ns else null


def alt(x, y):
    return lambda Ns: x(Ns) | y(Ns)


def star(x):
    return lambda Ns: opt(plus(x))(Ns)


def plus(x):
    return lambda Ns: genseq(x, star(x), Ns, startx=1)


def oneof(chars):
    set_chars = set(chars)
    return lambda Ns: set_chars if 1 in Ns else null


def seq(x, y):
    return lambda Ns: genseq(x, y, Ns)


def opt(x):
    return alt(epsilon, x)
