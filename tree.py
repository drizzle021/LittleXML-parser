class Node:
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children or []

    def __repr__(self):
        return f"Node({self.symbol})"

def build_parse_tree(rule_seq, rules, nonterminals):
    stack = []

    for rule in rule_seq:
        lhs, rhs = rules[rule]

        children = []
        for sym in rhs:
            if sym in nonterminals:
                children.append(stack.pop())
            else:
                children.append(Node(sym))

        children.reverse()
        stack.append(Node(lhs, children))

    assert len(stack) == 1
    return stack[0]

def print_tree(node, prefix="", is_last=True):
    connector = "└── " if is_last else "├── "
    print(prefix + connector + node.symbol)
    prefix += "    " if is_last else "│   "
    for i, child in enumerate(node.children):
        print_tree(child, prefix, i == len(node.children)-1)