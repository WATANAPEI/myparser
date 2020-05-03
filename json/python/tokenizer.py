from typing import NamedTuple, List
import re


class Token(NamedTuple):
    kind: str
    value: str
    line: int
    column: int


def tokenize(code: str) -> List[Token]:
    keywords = {'TRUE', 'FALSE', 'NULL', }
    token_spec = [
            ('NUMBER', r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?'),
            ('OPEN_BRA', r'{'),
            ('CLOSE_BRA', r'}'),
            ('OPEN_LIST', r'\['),
            ('CLOSE_LIST', r'\]'),
            ('COLON', r':'),
            ('COMMA', r','),
            ('STRING', r'".+?"'),
            ('KEYWORD', r'(?![" \t\n\r]).+'),
            ('NEWLINE', r'[\n\r]+'),
            ('WHITESPACE', r'[ \t]+'),
            ('MISMATCH', r'.'),
            ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
    line_num = 1
    line_start = 0
    token_list = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'STRING':
            value = value.strip('"')  # strip double quote
        elif kind == 'KEYWORD' and value.upper() in keywords:
            kind = 'KEYWORD'
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'WHITESPACE':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        token_list.append(Token(kind, value, line_num, column))

    return token_list


if __name__ == '__main__':
    json = '''
        {
          "links": {
            "self": "http://example.com/articles",
            "next": "http://example.com/articles?page[offset]=2",
            "last": "http://example.com/articles?page[offset]=10"
          }
        }
    '''

    for token in tokenize(json):
        print(token)
