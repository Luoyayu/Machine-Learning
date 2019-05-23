top = lambda stk: stk[-1]
pop = lambda stk: stk.pop()
push = lambda stk, value: stk.append(value)

action_table = {  # state=1 r; state=0 s; state=3 acc
    0: {"$": "acc"},
    1: {"id": "r2", "proc": "r2", "$": "r2"},
    2: {"id": "s11", "proc": "s3"},
    3: {"id": "s4"},
    4: {";": "s5"},
    5: {"id": "r6", "proc": "r6", "$": "r6"},
    6: {"id": "s11", "proc": "s3"},
    7: {";": "s8"},
    8: {"id": "s11", "proc": "s3", "s": "s9"},
    9: {";": "r4", "$": "r4"},
    10: {";": "s12", "$": "r1"},
    11: {":": "s14"},
    12: {"id": "s11", "proc": "s3"},
    13: {";": "s12", "$": "r3"},
    14: {"^": "s18", "integer": "s16", "real": "s17"},
    15: {";": "r5", "$": "r5"},
    16: {";": "r7", "$": "r7"},
    17: {";": "r8", "$": "r8"},
    18: {"^": "s18", "integer": "s16", "real": "s17"},
    19: {";": "r9", "$": "r9"},
}

goto_table = {
    1: {"P": 0, "M": 2},
    2: {"D": 10},
    5: {"N": 6},
    6: {"D": 7},
    8: {"D": 13},
    12: {"D": 13},
    14: {"T": 15},
    18: {"T": 19}
}


class LR0:
    def __init__(self, filename):
        self.left_symbol = ["PP", "P", "M", "D", "D", "D", "N", "T", "T", "T"] + ['' for i in range(50)]
        self.right_num = (1, 2, 0, 3, 7, 3, 0, 1, 1, 2)
        self.number = [0 for i in range(5)]
        self.Input_str_n = 0
        self.Input_str = [["" for j in range(50)] for i in range(100)]

        S = []

        def read(filename):
            with open(filename, 'r', encoding="utf-8") as f:
                print("open {}".format(filename))
                i, j = 0, 0
                for line in f:
                    import re
                    ss = re.split(r'([:;$ ])', line)
                    for s in ss:
                        if s.strip() not in [' ', '']:
                            S.append(s.strip())
            # print("输入分析", S)
            for s in S:
                if s == "end": break
                self.Input_str[i][j] = s
                print(self.Input_str[i][j], end=" ")

                if s == '$':
                    print("")
                    self.Input_str_n += 1
                    i += 1
                    j = 0
                    continue
                j += 1

        read(filename)

        def process():
            print("begin LR0 process")
            fp = open("LR0_output.txt", 'w')
            for i in range(0, self.Input_str_n):
                LR0_stk = []  # int stk
                push(LR0_stk, 1)
                symbol_stk = []  # string stk
                for k in range(0, 5): self.number[k] = 0

                print("开始分析 [{}]:".format(i), end=' ')
                for j in range(0, 100):
                    print(self.Input_str[i][j], end=' ')
                    if self.Input_str[i][j] == '$': break
                print("")

                have_done = 0
                for j in range(0, 100):
                    stk_top = top(LR0_stk)
                    Input_top = self.Input_str[i][have_done]
                    # if Input_top[0:2] == "id": Input_top = "id"
                    # print(stk_top, Input_top)
                    try:
                        res = action_table[stk_top]["id" if Input_top[0:2] == "id" else Input_top]
                        state = 3 if res == 'acc' else (0 if res[0] == 's' else 1)
                        if state == 3:
                            res = 0
                        else:
                            res = int(action_table[stk_top]["id" if Input_top[0:2] == "id" else Input_top][1:])
                    except KeyError:
                        res = 0
                        state = -1

                    # print("res:", res)
                    # print("state:", state)
                    if state == 3:
                        print("END\n")
                        fp.write("end\n")
                        break

                    if state == -1:
                        exit("error")

                    elif state == 0:
                        push(symbol_stk, Input_top)
                        have_done += 1
                        push(LR0_stk, res)

                    elif state == 1:
                        print(res, end=" ")
                        fp.write(str(res) + " ")
                        for kk in range(0, self.right_num[res]):
                            print(top(symbol_stk), end=" ")
                            fp.write(top(symbol_stk) + " ")

                            pop(symbol_stk)
                            pop(LR0_stk)

                        def add_number(s):
                            n = -1
                            if s == 'P':
                                n = 0
                            elif s == 'D':
                                n = 1
                            elif s == 'T':
                                n = 2
                            elif s == 'M':
                                n = 3
                            elif s == 'N':
                                n = 4
                            else:
                                return s
                            s += str(self.number[n])
                            self.number[n] += 1
                            return s

                        str_tmp = add_number(self.left_symbol[res])
                        print("<= " + str_tmp)
                        fp.write(str_tmp + " ")
                        fp.write("over\n")
                        push(symbol_stk, str_tmp)
                        push(LR0_stk, goto_table[top(LR0_stk)][self.left_symbol[res]])

            fp.write("FINISH\n")
            print("======LR0分析结束======")

        process()


class symbol:
    def __init__(self, n=None, t=None, o=None, newtable=None):
        self.name = n
        self.type = t
        self.offset = o
        self.newtable = None


class symbol_list:
    def __init__(self):
        self.symbol_n = 0
        self.sl = [symbol() for i in range(100)]
        self.save_sum = 0

    def symbol_add(self, name, type, width, newtable):
        self.sl[self.symbol_n] = symbol(name, type, width, newtable)
        self.symbol_n += 1

    def symbol_list_show(self):
        print("====symbol_list=====")
        for i in range(0, self.symbol_n):
            if not (self.sl[i].offset + 1 == 0):
                print("name:", self.sl[i].name, "\ttype:", self.sl[i].type,
                      "\toffset:", self.sl[i].offset)
            else:
                print("name:", self.sl[i].name, "\tnew table:", self.sl[i].newtable)

    def symbol_addwidth(self):
        self.save_sum = 0
        for i in range(0, self.symbol_n):
            self.save_sum += self.sl[i].offset


class item:
    def __init__(self, n=None, t=None, w=None):
        self.name = n
        self.type = t
        self.width = w


class sen_translate:
    def __init__(self, filename):
        self.Input_str_k = 0
        self.Input_str = [[["" for i in range(100)] for i in range(100)] for i in range(100)]
        self.Input_str_n = [0 for i in range(10)]
        self.item_n = 0
        self.item_list = [item() for i in range(100)]

        self.symbol_stk = []  # symboll_list stk
        self.offset_stk = []
        for i in range(0, 10): self.Input_str_n[i] = 0

        self.read(filename)
        self.process()

    def read(self, filename):
        S = []
        with open(filename, 'r', encoding="utf-8") as f:
            i, j = 0, 0

            for line in f:
                import re
                ss = re.split(r"([ ;:])", line)
                for s in ss:
                    if s.strip() not in ['', ' ']:
                        S.append(s.strip())
            # print("LR0分析规约", S)
            for line in S:
                if line == "FINISH": break

                if line == "end":
                    self.Input_str_k += 1
                    i = 0
                    continue
                self.Input_str[self.Input_str_k][i][j] = line
                if line == "over":
                    self.Input_str_n[self.Input_str_k] += 1
                    i += 1
                    j = 0
                    continue
                j += 1

    def item_add(self, name, type, width):
        # print(self.item_n, name, type, width)
        self.item_list[self.item_n] = item(name, type, width)
        self.item_n += 1

    def item_list_show(self):
        print("======item table=======", self.item_n)
        for i in range(0, self.item_n):
            print("name:", self.item_list[i].name, "\ttype:", self.item_list[i].type, end="")

            if self.item_list[i].width != -1:
                print("\twidth: ", self.item_list[i].width, end="")
            print("")

    def item_search(self, name):
        for i in range(0, self.item_n):
            # print(self.item_list[i].name, end=" ")
            if self.item_list[i].name == name:
                # print("match", name)
                return self.item_list[i]

        exit("error! can't find {} in item list\n".format(name))

    def process(self):
        # print(self.Input_str_k)
        for k in range(0, self.Input_str_k):
            for i in range(0, self.Input_str_n[k]):
                j = 0
                while self.Input_str[k][i][j] != 'over':
                    print(self.Input_str[k][i][j], end=" ")
                    j += 1
                print("")

            for i in range(0, self.Input_str_n[k]):
                # print(self.Input_str[k][i][0])
                if self.Input_str[k][i][0] == '1':
                    tmp_list = top(self.symbol_stk)
                    tmp_list.symbol_addwidth()

                    print("show item and offset stk")
                    self.item_list_show()
                    while not (len(self.symbol_stk) == 0):
                        tmp = top(self.symbol_stk)
                        pop(self.symbol_stk)
                        tmp.symbol_list_show()

                    print("=====offset list======")
                    while not (len(self.offset_stk) == 0):
                        tmp = top(self.offset_stk)
                        pop(self.offset_stk)
                        print(tmp)

                elif self.Input_str[k][i][0] == '2':
                    push(self.symbol_stk, symbol_list())
                    push(self.offset_stk, 0)

                elif self.Input_str[k][i][0] == '3':
                    pass

                elif self.Input_str[k][i][0] == '4':
                    temp_list1 = top(self.symbol_stk)
                    temp_list1.symbol_addwidth()

                    pop(self.symbol_stk)
                    pop(self.offset_stk)

                    temp_list = top(self.symbol_stk)
                    temp_list.symbol_add(self.Input_str[k][i][6], "", -1, temp_list1)

                elif self.Input_str[k][i][0] == '5':
                    self.item_add(self.Input_str[k][i][3], "id.type", -1)

                    temp_t = self.item_search(self.Input_str[k][i][1])

                    top_offset = top(self.offset_stk)
                    temp_list = top(self.symbol_stk)

                    temp_list.symbol_add(self.Input_str[k][i][3], temp_t.type, top_offset, None)

                    pop(self.offset_stk)
                    push(self.offset_stk, top_offset + temp_t.width)

                elif self.Input_str[k][i][0] == '6':
                    push(self.symbol_stk, symbol_list())
                    push(self.offset_stk, 0)

                elif self.Input_str[k][i][0] == '7':
                    self.item_add(self.Input_str[k][i][2], "integer", 4)

                elif self.Input_str[k][i][0] == '8':
                    self.item_add(self.Input_str[k][i][2], "real", 8)

                elif self.Input_str[k][i][0] == '9':
                    temp_item = self.item_search(self.Input_str[k][i][1])

                    print(temp_item.name, temp_item.type)
                    self.item_add(self.Input_str[k][i][3], temp_item.type + '*', 4)

            print("run succ\n\n")


if __name__ == '__main__':
    lr0 = LR0("LR0file.txt")
    sen_translate1 = sen_translate("LR0_output.txt")
