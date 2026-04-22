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
                if stack:
                    children.append(stack.pop())
                else:
                    children.append(Node("ERROR"))
            else:
                children.append(Node(sym))

        children.reverse()
        stack.append(Node(lhs, children))

    if len(stack) != 1:
        print("Warning: incomplete tree due to errors")

    return stack[0] if stack else Node("EMPTY")

def print_tree(node, prefix="", is_last=True):
    connector = "└── " if is_last else "├── "
    print(prefix + connector + node.symbol)
    prefix += "    " if is_last else "│   "
    for i, child in enumerate(node.children):
        print_tree(child, prefix, i == len(node.children)-1)

import matplotlib.pyplot as plt

def get_height(node):
    if not node.children:
        return 1
    return sum(get_height(child) for child in node.children)

def layout_tree(node, depth=0, y=0, positions=None):
    if positions is None:
        positions = {}

    height = get_height(node)
    positions[node] = (depth, y)

    current_y = y - height / 2
    for child in node.children:
        child_h = get_height(child)
        child_y = current_y + child_h / 2

        layout_tree(child, depth + 1, child_y, positions)
        current_y += child_h

    return positions

def visualize_tree(root):
    positions = layout_tree(root)

    fig, ax = plt.subplots(figsize=(14, 10))

    for node, (x, y) in positions.items():
        ax.text(x, y, node.symbol, va='center', ha='left')
        for child in node.children:
            x2, y2 = positions[child]
            ax.plot([x, x2], [y, y2])

    ax.set_axis_off()
    plt.show()