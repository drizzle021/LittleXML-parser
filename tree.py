from colors import bcolors


class Node:
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children or []

    def __repr__(self):
        return f"Node({self.symbol})"

def print_tree(node, prefix="", is_last=True):
    connector = "└── " if is_last else "├── "

    is_leaf = len(node.children) == 0

    label = node.symbol

    if node.value is not None and node.value != node.symbol:
        label += f": {node.value}"

    if is_leaf:
        label = f"{bcolors.OKCYAN}{label}{bcolors.ENDC}"

    print(prefix + connector + label)

    prefix += "    " if is_last else "│   "
    for i, child in enumerate(node.children):
        print_tree(child, prefix, i == len(node.children) - 1)

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

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(14, 10))

    for node, (x, y) in positions.items():
        label = node.symbol
        if node.value is not None and node.value != node.symbol:
            label += f"\n({node.value})"

        ax.text(x, y, label, va='center', ha='left')

        for child in node.children:
            x2, y2 = positions[child]
            ax.plot([x, x2], [y, y2])

    ax.set_axis_off()
    plt.show()