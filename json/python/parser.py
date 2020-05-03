#! /bin/usr/python3

import tokenizer
from typing import List


def get_next_token(code, idx):
    return (code[idx+1], idx + 1)


def parse_main(code: List[tokenizer.Token], idx: int):
    next_token = code[idx]
    if next_token.kind == 'OPEN_BRA':
        return parse_obj(code, idx)
    elif next_token.kind == 'OPEN_LIST':
        return parse_list(code, idx)


def parse_obj(code: List[tokenizer.Token], idx: int):
    '''
    Suppose current token and index(idx) point to the
    open bracket or comma.
    '''
    pair = []
    next_token, idx = get_next_token(code, idx)
    if next_token.kind == 'CLOSE_BRA':
        return ({}, idx+1)

    while True:
        if next_token.kind == 'STRING':
            key = next_token.value
        else:
            raise Exception("key token is exptected after bracket")

        next_token, idx = get_next_token(code, idx)
        if next_token.kind != 'COLON':
            raise Exception("colon must come after key token")

        next_token, idx = get_next_token(code, idx)
        if next_token.kind not in ['NUMBER', 'OPEN_BRA', 'OPEN_LIST', 'STRING', 'KEYWORD']:
            raise Exception("value should comde after colon")
        if next_token.kind in ['NUMBER', 'STRING', 'KEYWORD']:
            pair.append((key, next_token.value))

        next_token, idx = get_next_token(code, idx)
        if next_token.kind == 'CLOSE_BRA':
            break
        else:
            next_token, idx = get_next_token(code, idx)


def parse_list(code: List[tokenizer.Token], idx: int):
    _ = 1
