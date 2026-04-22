from load_parse_table import load_parse_table
from rules import rules
from parser import parse
from tree import build_parse_tree, print_tree, visualize_tree
from lexer import tokenize
import sys
import examples

PARSE_TABLE = load_parse_table(path="table.csv")
GRAMMAR_RULES = rules
START_SYMBOL = "xmldokument"
EOF = "$"
SRC = examples.src
TOKENS = tokenize(SRC)

print(f"Input:  {SRC}")
print(f"Tokens: {TOKENS}\n")

success, rule_seq = parse(
    TOKENS, 
    PARSE_TABLE, 
    GRAMMAR_RULES, 
    START_SYMBOL, 
    EOF=EOF,
    sync={"<",">","/>","</","$"},
    recovery=True
)
print(f"Success: {success}, Rule sequence: {rule_seq}")

# If parsing fails, exit without trying to build a tree
# Comment this to see where errors occur in the tree
if not success:
    print("Parsing failed. No parse tree generated.")
    sys.exit(1)

nonterminals = set(PARSE_TABLE.keys())

lhs_of = {}
for nt, row in PARSE_TABLE.items():
    for tok, rule in row.items():
        lhs_of[rule] = nt


print("Parse tree:")
tree = build_parse_tree(rule_seq[::-1], GRAMMAR_RULES, nonterminals)
print_tree(tree)
visualize_tree(tree)