# TODO implement and log recovery
def parse(tokens, table, rules, start_symbol, EOF='$'):
    '''
        Parse the input tokens using pushown automaton.
        Returns a tuple containing success boolean and a list of rule indeces used to generate the input string.
    '''
    stack = [EOF, start_symbol]
    i = 0
    rule_seq = []

    while True:
        top = stack.pop()
        curr_token = tokens[i]
        print(f"\nStack: {stack}, Current token: {curr_token}, Top: {top}")

        '''
            Empty stack and end of input -> accept the input string.
        '''
        if top == EOF and curr_token == EOF:
            return True, rule_seq
        
        '''
            Generated input symbol matches current token, shift the input.
        '''
        if top == curr_token:
            i += 1
            continue
        '''
            Apply production rule from the parse table.
        '''
        if top in table:
            rule = table[top].get(curr_token)
            if not rule:
                return False, rule_seq
            production = rules[rule][1]

            print(f"Applying rule {rule}: {top} -> {' '.join(production)}")

            stack.extend(reversed(production))
            rule_seq.append(rule)
            continue
        '''
            Error -> deny the input string.
        '''
        return False, rule_seq