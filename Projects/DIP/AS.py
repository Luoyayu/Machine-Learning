from termcolor import cprint

tables = {'begin': 1, 'if': 2, 'then': 3, 'while': 4, 'do': 5, 'end': 6, 'id': 10, 'num': 11, '+': 13, '-': 14, '*': 15,
          '/': 16, ':': 17, ':=': 18, '<': 20, '<>': 21, '<=': 22, '>': 23, '>=': 24, '=': 25, ';': 26, '(': 27,
          ')': 28, '#': 0}
rw = {'begin', 'if', 'then', 'while', 'do', 'end'}
end_char = {'+', '-', '*', '/', ':', '(', ')', ';', '>', '<', '=', '#', ' ', '\t', '\n'}
blank_char = {' ', '\t', '\n'}


def LA(raw_code):
    """
    :param raw_code: 源程序
    :return: None
    """
    i, lsti, l, error_cnt, flag = 0, len(raw_code) - 1, 1, 0, 0
    while i < len(raw_code):
        x = raw_code[i]  # print(repr(x))
        if x in blank_char:
            i += 1
            if x == '\n': l += 1
            continue
        if x.isalpha() or x.isdigit():  # 读入单词的首位是字母或数字
            syn, j, word = tables['id'] if x.isalpha() else tables['num'], i + 1, x
            while j <= lsti and raw_code[j] not in end_char:
                if not raw_code[j].isalpha() and not raw_code[j].isdigit() and raw_code[
                    j] not in tables.keys():  # 读入过程中有非法字符
                    break
                if x.isdigit() and raw_code[j].isalpha():  # 单词首位为数字, 却读入字母
                    error_cnt += 1
                    cprint("{}:{}: error: invalid suffix '{}' on integer constant!".format(__file__, l, raw_code[j]),
                           'red')
                    flag = 1
                    break
                else:
                    word, j = word + raw_code[j], j + 1
            i += len(word)
            if x.isalpha() and word in rw:  # 判断单词是否是保留字
                syn = tables[word]
            if not flag:
                print('({},{})'.format(syn, word))
        else:  # 如果读入的单词是特殊符号
            if x not in tables.keys():
                # 不在table中的是非法单词
                cprint("{}:{}: error: stray '{}' in program".format(__file__, l, x), 'red')
                error_cnt += 1
                i += 1
                continue
            elif i != lsti and (x + raw_code[i + 1]) in tables.keys():  # 如果当前特殊字符与下一位组成运算符
                x, i = x + raw_code[i + 1], i + 1
            i, syn = i + 1, tables[x]
            print('({},{})'.format(syn, x))
    if not error_cnt:
        cprint('success!\n', 'green')
    else:
        cprint('find {} error(s)\n'.format(error_cnt), 'red')


def test():
    print(tables.keys())
    test_code1 = r"begin x:=9; if x>9 then x:=2*x+1/3; end #"
    test_code2 = """while:@
	begin@
		print(String);@
	end@
end@
"""
    test_code3 = """@=1a#
    begin        #a=1#
    a=(1-1<>0)  ;end#
    """
    test_code4 = """while:
    begin
        print(String);
    end
end
    """
    test_code = [test_code1, test_code2, test_code3, test_code4]
    for x in test_code:
        cprint('源程序:\n%s' % x, 'blue'), LA(x)
        cprint('++++++++++++++++++++++++++++++++++++++++++++++', 'grey')


def testMain():
    test_code1 = "abc;ed-23, abc;"
    test_code2 = "abc;de-23; abc;"
    test_code3 = "begin x:=9ab; if x>    <9 then x<>2*x+1/3;, end #"
    test_code = [test_code1, test_code2, test_code3]
    for x in test_code:
        cprint('源程序:\n%s' % x, 'blue'), LA(x)
        cprint('++++++++++++++++++++++++++++++++++++++++++++++', 'grey')


def main():
    raw_code = ""
    try:
        while True:
            raw_code += input() + '\n'
    except EOFError:
        print("input string: %s\nLA:" % raw_code)
        LA(raw_code)
        return


if __name__ == '__main__':
    testMain()
    main()
