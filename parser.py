import re

token_specification = [
    ('str',      r'[\'"](.*?)[\'"]'),
    ('int',      r'\d+$'),
    ('float',    r'\d+\.\d+'),
    ('bool',     r'True|False'),
    ('NoneType', r'NoneType'),
    ('ID',       r'[A-Za-z]+'),
]

def tokenize(word: str) -> tuple:
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    
    kind = ''
    value = ''

    for mo in re.finditer(tok_regex, word):
        kind = mo.lastgroup
        value = mo.group()
 
    return kind, value

def calcul_tokenize(calcul: str) -> list:
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    parsed_calcul = []

    for mo in re.finditer(tok_regex, calcul):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'INTEGER':
            parsed_calcul.append(value)
        elif kind == 'OP':
            parsed_calcul.append(value)
        elif kind == 'SKIP':
            continue
    
    return parsed_calcul