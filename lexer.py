SINGLE_CHAR_TOKENS = set('<>.-:_!@#')


def tokenize(text):
    '''
    Converts a raw LittleXML string into a token sequence for the parser.
    Each letter -> IDENT, each digit -> NUMBER, whitespace is skipped.
    Returns a list ending with the EOF sentinel '$'.
    '''
    tokens = []
    i = 0
    n = len(text)

    while i < n:
        if text[i].isspace():
            i += 1
            continue

        # Multi-character tokens — longest match first
        if text[i:i+5] == '<?xml':
            tokens.append('<?xml')
            i += 5
            continue

        if text[i:i+8] == 'version=':
            tokens.append('version=')
            i += 8
            continue

        if text[i:i+2] == '?>':
            tokens.append('?>')
            i += 2
            continue

        if text[i:i+2] == '</':
            tokens.append('</')
            i += 2
            continue

        if text[i:i+2] == '/>':
            tokens.append('/>')
            i += 2
            continue

        c = text[i]

        if c.isalpha():
            tokens.append('IDENT')
            i += 1
            continue

        if c.isdigit():
            tokens.append('NUMBER')
            i += 1
            continue

        if c in SINGLE_CHAR_TOKENS:
            tokens.append(c)
            i += 1
            continue

        raise ValueError(f"Unexpected character '{c}' at position {i}")

    tokens.append('$')
    return tokens


if __name__ == '__main__':
    examples = [
        '<a/>',
        '<?xml version=1.0?><a/>',
        '<?xml version=12.3?><ab:><ef:>N@C#</ab:></ab:>',
        '<a>Hello123</a>',
    ]
    for ex in examples:
        print(f"Input:  {ex}")
        print(f"Tokens: {tokenize(ex)}")
        print()
