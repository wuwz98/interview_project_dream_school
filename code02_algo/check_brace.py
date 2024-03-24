def check_brackets(input_str):
    stack = []
    result = []

    for i, char in enumerate(input_str):
        if char == '(':
            stack.append((char, i))
            result.append(' ')
        elif char == ')':
            if stack:
                result.append(' ')
                stack.pop()
            else:
                result.append('?')
        else:
            result.append(' ')
            continue

    while stack:
        tup = stack.pop()
        result[tup[1]] = 'x'

    return ''.join(result)

if __name__ == '__main__':
    lines = open("test_cases.txt", 'r').read().splitlines()
    for line in lines:
        res = check_brackets(line)
        print(line)
        print(res)