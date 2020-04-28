#! /usr/bin/python3

def tokenize(contents):
    list = []
    i = 0
    for i, c in enumerate(contents):
        if c == '{' or c == '}':
            list.append(c)
        if c == '"' or c == "'":
            word = ""
            next = contents[i+1]
            while(next != '"'):
                word += next
                i = i+1
                next = contents[i]
            print(word)
            list.append(word)


    return list


if __name__ == '__main__':
    with open('./test.json') as f:
        contents = f.read()
        #print(contents)
        list = tokenize(contents)
        for l in list:
            print('{}, '.format(l))


