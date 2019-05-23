from termcolor import cprint

error = lambda attach_warning: cprint("Error! " + attach_warning, 'red')
top = lambda stk: stk[-1]

M = {
    "E": {
        'i': ['T', "E'"],
        '(': ['T', "E'"],
        ')': ['synch'],
        '$': ['synch']
    },
    "E'": {
        '+': ['+', 'T', "E'"],
        ')': ['ε'],
        '$': ['ε']
    },
    "T": {
        'i': ['F', "T'"],
        '(': ['F', "T'"],
        '+': ['synch'],
        ')': ['synch'],
        '$': ['synch']
    },
    "T'": {
        "+": ['ε'],
        "*": ['*', 'F', "T'"],
        ")": ['ε'],
        "$": ['ε']
    },
    "F": {
        'i': ['i'],
        '(': ['(', 'E', ')'],
        '+': ['synch'],
        '*': ['synch'],
        ')': ['synch'],
        '$': ['synch']
    }
}

end_char = ['i', ' ', '\t', '\n', 'ε', '(', ')', '+', '*']


def check_LL1(r, dg=False):
    error_cnt = 0
    r = r.replace(' ', '')
    cprint('开始预测分析 {}'.format(r[:-1]), color="blue", attrs=['concealed'])
    stk = ['$', 'E']
    X = top(stk)
    ip = 0
    while X != '$':
        if dg: cprint('当前栈 {}'.format(stk), 'yellow')
        a = r[ip]
        if X == a:
            stk.pop()
            ip += 1
            cprint('匹配 {}'.format(a), 'green')
        elif X in end_char:  # X is an end char
            error_cnt += 1
            error('{} is end char'.format(X))
            if X != a:
                cprint("Error! 栈顶为未终结符且栈顶符号与输入符号不符!", 'red')
                stk.pop()
        elif M[X].get(a) is None:  # 分析表入口为空 # No move M(X,a)
            error_cnt += 1
            # error('No Move[{}, {}]'.format(X, a))
            cprint("Error! 分析表入口为空, 跳过输入符号 {}".format(a), 'red')
            ip += 1
        elif M[X].get(a) == ['synch']:  # 分析表入口为synch
            cprint("Error! 对于输入符号 {}, 分析表入口为synch, 弹出 {}".format(a, X), 'red')
            stk.pop()
        else:
            Y = M[X].get(a)
            cprint("输出 {} -> {}".format(X, ''.join(Y)), 'magenta')
            stk.pop()
            for y in Y[::-1]:
                if y != 'ε' and y != 'synch':
                    stk.append(y)  # push reversed Y
        X = top(stk)
    return error_cnt == 0  # if no error


def main(flag=1, raw_input=None, dg=False):
    while True and flag:
        raw_input = input('输入以$结尾的语法串')
        if raw_input[-1] != '$':
            cprint("Do you mean {}$ ?".format(raw_input), "blue", end="")
            if input("[y/n]") == 'y':
                raw_input += "$"
                break
            else:
                continue
    if check_LL1(raw_input, dg):
        cprint('legal input!\n', 'blue', attrs=['bold', 'underline', ])
    else:
        cprint('illegal input!\n', 'blue', attrs=['bold', 'underline', ])


def test():
    main(flag=0, raw_input="i + i*i$", dg=True)
    main(0, "(i+i)*(i+i)$")
    main(0, "i*(i+i)$")
    main(0, "((i)*(i))$")
    main(0, "i(i*i)$")
    main(0, "(i+i*i$")
    main(0, "+i*+i$")
    pass


def maintest():
    main(0, "i++i**i$")
    main(0, "(i+i*i)+i$")
    main(0, " i+i*i+.$")


if __name__ == '__main__':
    maintest()
    main()
