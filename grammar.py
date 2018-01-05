'''
Grammar and parser
'''

import decorator


def grammar(description, whitespace=r'\s*'):
    '''
    Convert a description to a grammar.
    '''
    G = {' ': ([whitespace], )}
    description = description.replace('\t', ' ')  # no tabs
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G


def split(text, sep=None, maxsplit=-1):
    "Like str.split applied to text, but strips whitespace from each piece."
    result = [t.strip() for t in text.strip().split(sep, maxsplit) if t]
    return result


G = grammar(r'''
Exp     => Term [+-] Exp | Term
Term    => Factor [*/] Term | Factor
Factor  => Funcall | Var | Num | [(] Exp [)]
Funcall => Var [(] Exps [)]
Exps    => Exp [,] Exps | Exp
Var     => [a-zA-Z_]\w*
Num     => [-+]?[0-9]+([.][0-9]*)?
''')


def verify(G):
    lhstokens = set(G) - set([' '])
    rhstokens = set(t for alts in G.values() for alt in alts for t in alt)

    def show(title, tokens):
        print(title, '=', ' '.join(sorted(tokens)))

    show('Non-Term', G)
    show('Terminals', rhstokens - lhstokens)
    show('Suspects', [t for t in (rhstokens - lhstokens) if t.isalnum()])
    show('Orphans', lhstokens - rhstokens)


Fail = (None, None)


def parse(start_symbol, text, grammar):
    '''
    Parse text with symbol use grammar.
    '''
    import re
    tokenizer = grammar[' '][0][0] + '(%s)'

    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None:
                return Fail
            result.append(tree)
        return result, text

    @decorator.memo
    def parse_atom(atom, text):
        if atom in grammar:
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None:
                    return [atom] + tree, rem
            return Fail
        else:
            m = re.match(tokenizer % atom, text)
            return Fail if not m else (m.group(1), text[m.end():])

    return parse_atom(start_symbol, text)


def test():
    assert parse('Exp', 'x * 3', G) == ([
        'Exp', [
            'Term', ['Factor', ['Var', 'x']], '*',
            ['Term', ['Factor', ['Num', '3']]]
        ]
    ], '')
    assert parse('Exp', 'a * x', G) == ([
        'Exp', [
            'Term', ['Factor', ['Var', 'a']], '*',
            ['Term', ['Factor', ['Var', 'x']]]
        ]
    ], '')
    print('test success')


if __name__ == '__main__':
    test()
    # verify(G)
