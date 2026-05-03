from token_ import Token
from colors import bcolors

# DFA transition table: TRANSITIONS[state][char] = next_state
TRANSITIONS = {
    'START':   {'<': 'LT', '?': 'Q', '/': 'SL', 'v': 'V'},
    'LT':      {'?': 'LT_Q', '/': 'LT_SL'},
    'LT_Q':    {'x': 'LT_QX'},
    'LT_QX':   {'m': 'LT_QXM'},
    'LT_QXM':  {'l': 'LT_QXML'},
    'Q':       {'>': 'Q_GT'},
    'SL':      {'>': 'SL_GT'},
    'V':       {'e': 'VE'},
    'VE':      {'r': 'VER'},
    'VER':     {'s': 'VERS'},
    'VERS':    {'i': 'VERSI'},
    'VERSI':   {'o': 'VERSIO'},
    'VERSIO':  {'n': 'VERSION'},
    'VERSION': {'=': 'VERSION_EQ'},
}

# Accepting states and their token types
ACCEPT = {
    'LT': '<', 'LT_SL': '</', 'LT_QXML': '<?xml',
    'Q_GT': '?>', 'SL_GT': '/>',
    '>': '>', '.': '.', '-': '-', ':': ':', '_': '_',
    '!': '!', '@': '@', '#': '#',
    'LETTER': 'LETTER', 'NUMBER': 'NUMBER',
    'V': 'LETTER', 'VERSION_EQ': 'version=',
}

def _next(state, c):
    t = TRANSITIONS.get(state, {}).get(c)
    if t:
        return t
    if state == 'START':
        if c in '>.-:_!@#': return c
        if c.isalpha(): return 'LETTER'
        if c.isdigit(): return 'NUMBER'
    return None

def tokenize(text):
    '''
    Converts a raw LittleXML string into a token sequence for the parser.
    Implements a DFA with maximal munch and error recovery by skipping invalid characters.
    Returns a list ending with the EOF sentinel '$'.
    '''
    tokens = []
    errors = 0
    i = 0
    n = len(text)

    while i < n:
        if text[i].isspace():
            i += 1
            continue

        # Maximal munch: advance until no transition, emit last accepted token
        state = 'START'
        last_accept = None
        last_pos = i
        j = i
        while j < n:
            c = text[j]
            ns = _next(state, c)
            if ns in ACCEPT:
                print(f"  {bcolors.OKCYAN}State: {state}, Char: '{c}', Next: {ns} (accept: {ACCEPT[ns]}){bcolors.ENDC}")
            else:
                print(f"  State: {state}, Char: '{c}', Next: {ns or '-'}")
            if ns is None:
                break
            state = ns
            j += 1
            if state in ACCEPT:
                last_accept = state
                last_pos = j

        if last_accept is None:
            print(f"{bcolors.FAIL}LEX ERROR: unexpected '{text[i]}' at position {i}, skipping.{bcolors.ENDC}")
            errors += 1
            i += 1
            continue
            
        token = Token(ACCEPT[last_accept], text[i:last_pos])
        print(f"{bcolors.OKCYAN}Token: {token}{bcolors.ENDC}")
        tokens.append(token)
        i = last_pos

    tokens.append(Token('$', '$'))
    if errors:
        print(f"{bcolors.WARNING}Tokenization complete with {errors} error(s): {len(tokens) - 1} token(s).{bcolors.ENDC}")
    else:
        print(f"{bcolors.OKGREEN}Tokenization complete: {len(tokens) - 1} token(s).{bcolors.ENDC}")
    return tokens
