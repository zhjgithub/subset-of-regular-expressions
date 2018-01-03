null = frozenset()
dot = oneof('?')
epsilon = lit('')


def lit(s):
    return lambda Ns: set([s]) if len(s) in Ns else null


def alt(x, y):
    return lambda Ns: x(Ns) | y(Ns)


def star(x):
    return lambda Ns: opt(plus(x))(Ns)


def plus(x):
    return lambda Ns: genseq(x, star(x), Ns, startx=1)


def oneof(chars):
    return lambda Ns: set(chars) if 1 in Ns else null


def seq(x, y):
    return lambda Ns: genseq(x, y, Ns)


def opt(x):
    return alt(epsilon, x)
