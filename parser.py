from typing import List, Dict, Tuple, Set
from colors import bcolors  


class Node:
    def __init__(self, symbol, value=None):
        self.symbol = symbol
        self.value = value
        self.children = []

    def __repr__(self):
        return f"Node({self.symbol}, {self.value})"


def parse(
        tokens:List,
        table:Dict[str, Dict[str, int]],
        rules:Dict[int, Tuple[str, List[str]]],
        start_symbol:str,
        EOF:str='$',
        sync:Set[str]=set(),
        recovery:bool=True
        ) -> Tuple[bool, List[int], Node]:
     
    '''
        Parse the input tokens using pushown automaton with panic mode recovery.
        Returns a tuple containing success boolean, a list of rule indeces used to generate the input string,
        and the parse tree root.
    '''

    SYNC_TOKENS = sync
    root = Node(start_symbol)
    stack = [(EOF, None), (start_symbol, root)]
    i = 0
    rule_seq = []
 
    while True:
        top, node = stack.pop()
        curr_token = tokens[i]

        print(f"Stack: {[s for s, _ in stack]}, Current token:{curr_token}, Top: {top}")

        if top == EOF and curr_token.type != EOF:
            print(f"{bcolors.FAIL}ERROR: Unexpected symbol {curr_token} after end of document.{bcolors.ENDC}")
            return False, rule_seq, root
 
        '''
            Empty stack and end of input -> accept the input string.
        '''
        if top == EOF and curr_token.type == EOF:
            print(f"{bcolors.OKGREEN}Accepted input{bcolors.ENDC}")
            return True, rule_seq, root
         
        '''
            Generated input symbol matches current token, shift the input.
        '''
        if top == curr_token.type:
            if node is not None:
                node.value = curr_token.value
            i += 1
            continue

        '''
            Apply production rule from the parse table.
        '''
        if top in table:
            rule = table[top].get(curr_token.type)

            if not rule:
                if not recovery:
                    print(f"{bcolors.FAIL}ERROR: No rule for ({top}, {curr_token}).{bcolors.ENDC}")
                    return False, rule_seq, root

                print(f"{bcolors.FAIL}ERROR: No rule for ({top}, {curr_token}). Entering panic mode.{bcolors.ENDC}")

                while curr_token.type not in SYNC_TOKENS:
                    print(f"{bcolors.WARNING}Skipping token: {curr_token}{bcolors.ENDC}")
                    i += 1
                    if i >= len(tokens):
                        return False, rule_seq, root
                    curr_token = tokens[i]

                print(f"{bcolors.OKGREEN}Found sync token: {curr_token}. Resuming parsing.{bcolors.ENDC}")
                continue

            lhs, production = rules[rule]

            print(f"{bcolors.OKCYAN}Applying rule {rule}: {top} -> {' '.join(production)}{bcolors.ENDC}")

            if len(production) == 0:
                if node is not None:
                    node.children = []
            else:
                children = [Node(sym) for sym in production]

                if node is not None:
                    node.children = children

                stack.extend(reversed(list(zip(production, children))))

            rule_seq.append(rule)
            continue

        else:
            '''
            Error -> try to recover or deny the input string.
            '''
            if not recovery:
                print(f"{bcolors.FAIL}ERROR: Unexpected symbol {curr_token} when expecting {top}.{bcolors.ENDC}")
                return False, rule_seq, root

            print(f"{bcolors.FAIL}ERROR: Unexpected symbol {curr_token} when expecting {top}. Entering panic mode.{bcolors.ENDC}")

            while curr_token.type not in SYNC_TOKENS:
                print(f"  {bcolors.WARNING}Skipping token: {curr_token}{bcolors.ENDC}")
                i += 1
                if i >= len(tokens):
                    return False, rule_seq, root
                curr_token = tokens[i]

            print(f"  {bcolors.OKGREEN}Found sync token: {curr_token}. Resuming parsing.{bcolors.ENDC}")
            continue