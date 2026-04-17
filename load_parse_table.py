import csv

def load_parse_table(path="table.csv"):
    '''
        Loads parse table from CSV file containing nonterminals as rows and input symbols as columns.
        Maps the rule indeces to pairs of nonterminals and input symbols.
        Outputs a dictonary in the form {nonterminal: {input symbols: rule_index}}.
    '''
    table = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)[1:]

        for row in reader:
            nonterminal = row[0].strip()
            table[nonterminal] = {}

            for terminal, value in zip(headers, row[1:]):
                value = value.strip()
                if value:
                    table[nonterminal][terminal] = int(value)

    return table

if __name__ == "__main__":
    from pprint import pprint
    import json
    pprint(load_parse_table())
    json.dump(load_parse_table(), open("table.json", "w", encoding="utf-8"), indent=4)
