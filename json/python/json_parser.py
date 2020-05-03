#! /usr/bin/python3
from typing import List
import tokenizer
import parser


def tokenize_orig(contents):
    list = []
    i = 0
    while(i != len(contents)-1):
        c = contents[i]
        if c == ' ' or c == '\t':
            i += 1
            continue

        if c == '{' or c == '}':
            list.append(c)

        if c == '[' or c == ']':
            list.append(c)

        if c == ',':
            list.append(c)

        if c == '"' or c == "'":
            quotation_char = c
            word = ""

            # extract word between quotation
            while True:
                i += 1
                word += contents[i]
                if contents[i+1] == quotation_char:
                    i += 1
                    break

            list.append(word)

        if c == ':':
            list.append(c)

        i += 1

    return list


def main():
    with open('./test.json') as f:
        contents = f.read()
        # print(contents)
        list: List[tokenizer.Token] = tokenizer.tokenize(contents)
        # for i, l in enumerate(list):
        #     print('#{}: {} '.format(i, l))
        obj = parser.parse_main(list, 0)
        print(obj)


def check_token():
    with open('./test.json') as f:
        contents = f.read()
        list: List[tokenizer.Token] = tokenizer.tokenize(contents)
        for i, l in enumerate(list):
            print('#{}: {} '.format(i, l))


if __name__ == '__main__':
    main()
