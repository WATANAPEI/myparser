from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


def tokenize(code):
    keywords = {'TRUE', 'FALSE', 'NULL', 'NaN', 'Infinity', '-Infinity'}
    token_spec = [
            ('NUMBER', r'\d+(\.\d*)?'),  # FIXME: exponential
            ('OPEN_BRA', r'{'),
            ('CLOSE_BRA', r'}'),
            ('COLON', r':'),
            ('COMMA', r','),
            ('ID', r'".+?"'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
            ('MISMATCH', r'.'),
            ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)


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
