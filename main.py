from load_parse_table import load_parse_table
from rules import rules
from pprint import pprint
from parser import parse
from tree import build_parse_tree, print_tree

PARSE_TABLE = load_parse_table(path="table1.csv")
GRAMMAR_RULES = rules

pprint (PARSE_TABLE)
# <?xml version=12.3?><ab:><ef:>N@C#</ab:></ab:>
# <a><b/><c/></a> 
# <a>Hello<b/>World</a>
# <?xml version=12.3?></a>
tokens = ["<?xml", "version=", "NUMBER", ".", "NUMBER", "?>", 
          "<", "IDENT",":", ">","<", "IDENT",":", ">", "IDENT", "@","IDENT","#","</","IDENT",":",">","</","IDENT",":",">",
          "$"]
# tokens = ["<","IDENT",">","<","IDENT","/>","<","IDENT","/>","</","IDENT",">","$"]
# tokens = ["<","IDENT",">","IDENT","<","IDENT","/>","IDENT","</","IDENT",">", "$"]
tokens = ["<?xml", "version=", "NUMBER", ".", "NUMBER", "?>", 
          "<","IDENT","/>",
          "$"]
success, rule_seq = parse(tokens, PARSE_TABLE, GRAMMAR_RULES, "xmldokument")
print(f"Success: {success}, Rule sequence: {rule_seq}")

nonterminals = set(PARSE_TABLE.keys())

lhs_of = {}
for nt, row in PARSE_TABLE.items():
    for tok, rule in row.items():
        lhs_of[rule] = nt


print("Parse tree:")
tree = build_parse_tree(rule_seq[::-1], GRAMMAR_RULES, nonterminals)
print_tree(tree)