from typing import List, Dict, Tuple, Set
from colors import bcolors  

def parse(
        tokens:List[str],
        table:Dict[str, Dict[str, int]],
        rules:Dict[int, Tuple[str, List[str]]],
        start_symbol:str,
        EOF:str='$',
        sync:Set[str]=set(),
        recovery:bool=True
        ) -> Tuple[bool, List[int]]:
     
    '''
        Parse the input tokens using pushown automaton with panic mode recovery.
        Returns a tuple containing success boolean and a list of rule indeces used to generate the input string.
    '''
    #print(f"{bcolors.UNDERLINE}Starting parsing for input: {' '.join(tokens)}{bcolors.ENDC}")
    SYNC_TOKENS = sync
    stack = [EOF, start_symbol]
    i = 0
    rule_seq = []
    terminals = []
 
    while True:
        top = stack.pop()
        curr_token = tokens[i]
        print(f"Stack: {stack}, Current token:{curr_token}, Top: {top}, Terminals:{terminals}")

        if top == EOF and curr_token.type != EOF:
            print(f"{bcolors.FAIL}ERROR: Unexpected symbol {curr_token} after end of document.{bcolors.ENDC}")
            return False, rule_seq
 
        '''
            Empty stack and end of input -> accept the input string.
        '''
        if top == EOF and curr_token.type == EOF:
            print(f"{bcolors.OKGREEN}Accepted input: {"".join(terminals)}{bcolors.ENDC}")
            return True, rule_seq
         
        '''
            Generated input symbol matches current token, shift the input.
        '''
        if top == curr_token.type:
            i += 1
            terminals.append(curr_token.value)
            continue
        '''
            Apply production rule from the parse table.
        '''
        if top in table:
            rule = table[top].get(curr_token.type)
            if not rule:
                if not recovery:
                    print(f"{bcolors.FAIL}ERROR: No rule for ({top}, {curr_token}).{bcolors.ENDC}")
                    return False, rule_seq
                print(f"{bcolors.FAIL}ERROR: No rule for ({top}, {curr_token}). Entering panic mode.{bcolors.ENDC}")
                while curr_token.type not in SYNC_TOKENS:
                    print(f"{bcolors.WARNING}Skipping token: {curr_token}{bcolors.ENDC}")
                    i += 1
                    curr_token = tokens[i]
                print(f"{bcolors.OKGREEN}Found sync token: {curr_token}. Resuming parsing.{bcolors.ENDC}")
                continue

            production = rules[rule][1]
 
            print(f"{bcolors.OKCYAN}Applying rule {rule}: {top} -> {' '.join(production)}{bcolors.ENDC}")
 
            stack.extend(reversed(production))
            rule_seq.append(rule)
            continue

        else:
            '''
            Error -> try to recover or deny the input string.
            '''
            if not recovery:
                print(f"{bcolors.FAIL}ERROR: Unexpected symbol {curr_token} when expecting {top}.{bcolors.ENDC}")
                return False, rule_seq
            print(f"{bcolors.FAIL}ERROR: Unexpected symbol {curr_token} when expecting {top}. Entering panic mode.{bcolors.ENDC}")
            while curr_token.type not in SYNC_TOKENS:
                print(f"  {bcolors.WARNING}Skipping token: {curr_token}{bcolors.ENDC}")
                i += 1
                curr_token = tokens[i]
            print(f"  {bcolors.OKGREEN}Found sync token: {curr_token}. Resuming parsing.{bcolors.ENDC}")
            continue
    