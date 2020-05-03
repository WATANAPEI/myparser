#! /bin/usr/python3

import tokenizer
from typing import List
import re

NUMBER_RE = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))


def _get_next_token(code, idx):
    return (code[idx+1], idx + 1)


def parse_main(code: List[tokenizer.Token], idx: int):
    token = code[idx]
    if token.kind == 'OPEN_BRA':
        return parse_obj(code, idx)
    elif token.kind == 'OPEN_LIST':
        return parse_list(code, idx)
    elif token.kind == 'KEYWORD':
        if token.value.upper() == 'TRUE':
            return True, idx+1
        elif token.value.upper() == 'FALSE':
            return False, idx+1
        elif token.value.upper() == 'NULL':
            return None, idx+1
    elif token.kind == 'NUMBER':
        mo = NUMBER_RE.match(token.value)
        if mo is not None:
            integer, fruction, exp = mo.groups()
            if fruction is None and exp is None:
                return int(integer), idx+1
            else:
                return float(mo.group()), idx+1


def parse_obj(code: List[tokenizer.Token], idx: int):
    '''
    Suppose current token and index(idx) point to the
    open bracket or comma.
    '''
    pair = []
    next_token, idx = _get_next_token(code, idx)
    if next_token.kind == 'CLOSE_BRA':
        return ({}, idx+1)

    while True:
        if next_token.kind == 'STRING':
            key = next_token.value
        else:
            raise Exception("key token is exptected after bracket")

        next_token, idx = _get_next_token(code, idx)
        if next_token.kind != 'COLON':
            raise Exception("colon must come after key token")

        next_token, idx = _get_next_token(code, idx)
        if next_token.kind not in ['NUMBER', 'OPEN_BRA', 'OPEN_LIST', 'STRING', 'KEYWORD']:
            raise Exception("value should comde after colon")
        elif next_token.kind == 'STRING':
            pair.append((key, next_token.value))
        elif next_token.kind in ['NUMBER', 'OPEN_BRA', 'OPEN_LIST', 'KEYWORD']:
            value, idx = parse_main(code, idx)
            pair.append((key, next_token.value))

        print(f'pair {idx}: {pair}')
        next_token, idx = _get_next_token(code, idx)
        if next_token.kind == 'CLOSE_BRA':
            break
        elif next_token.kind != 'COMMA':
            raise Exception('comma is expected after value token')
        else:
            # next token = string token(key)
            next_token, idx = _get_next_token(code, idx)

    pairs = dict(pair)
    return pairs, idx


def parse_list(code: List[tokenizer.Token], idx: int):
    next_token, idx = _get_next_token(code, idx)
    list = []
    if next_token.kind == 'CLOSE_LIST':
        return list, idx+1
    while True:
        if next_token.kind not in ['NUMBER', 'OPEN_BRA', 'OPEN_LIST', 'STRING', 'KEYWORD']:
            raise Exception('value is expected')
        elif next_token.kind == 'STRING':
            list.append(next_token.value)
        elif next_token.kind in ['NUMBER', 'OPEN_BRA', 'OPEN_LIST', 'KEYWORD']:
            value, idx = parse_main(code, idx)
            list.append(value)

        print(f'line {idx}: {list}')

        next_token, idx = _get_next_token(code, idx)
        if next_token.kind == 'CLOSE_LIST':
            break
        elif next_token.kind != 'COMMA':
            raise Exception('comma is expected to come')
        else:
            next_token, idx = _get_next_token(code, idx)

    return list, idx


