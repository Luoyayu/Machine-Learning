from termcolor import cprint

top = lambda stk: stk[-1]
pop = lambda stk: stk.pop()
push = lambda value, stk: stk.append(value)


class T_T:
    def __init__(self):
        self.type = None
        self.width = 0


class ID:
    def __init__(self):
        self.name = None


class sem_relu:
    def __init__(self):
        start = 'P'
        over = ['s', 'id', 'integer', 'real', ';', ':']
        self.D_idx = 1
        self.T_idx = 1
        self.gen_rule = {
            'P': ['MD'],
            'M': ['ε'],
            'D': ['D;D', 'proc id;N D;s', 'id:T'],
            'N': ['ε'],
            'T': ['integer', 'real', '↑T'],
        }
        self.tables = []
        self.tblptr = []
        self.offset = []

    def mktable(self, prev):
        table = [
            [prev, 0]
        ]
        self.tables.append(table)
        self.tblptr.append(len(self.tables))
        return len(self.tables)

    def enter(self, table, name, type, offset):
        self.tables[table].append(
            [name, type, offset]
        )

    def addwidth(self, table, width):
        for i in range(1, len(table)):
            try:
                width += table[i][2]
            except IndexError:
                pass
        table[0][-1] = width

    def enterproc(self, table, name, newtable):
        self.tables[table].appen(
            [name, newtable]
        )

    def P0(self):
        self.addwidth(top(self.tblptr), top(self.offset))
        pop(self.tblptr)
        pop(self.offset)

    def M0(self):
        t = self.mktable(None)
        push(t, self.tblptr)
        push(0, self.offset)

    def D0(self):
        pass

    def D1(self, id):
        t = top(self.tblptr)
        self.addwidth(t, top(self.offset))
        pop(self.tblptr)
        pop(self.offset)
        self.enterproc(top(self.tblptr), id.name, t)

    def D2(self, id, T):
        self.enter(top(self.tblptr), id.name, T.type, top(self.offset))
        self.offset[-1] = top(self.offset) + T.width

    def N0(self):
        t = self.mktable(top(self.tblptr))
        push(t, self.tblptr)
        push(0, self.offset)

    def T0(self):
        T = T_T()
        T.type = "integer"
        T.width = 4
        return T

    def T1(self):
        T = T_T()
        T.type = "real"
        T.width = 8
        return T

    def T2(self, T1):
        T = T_T()
        T.type = "pointer(" + str(T1.type) + ")"
        T.width = 4
        return T

    def parse(self):
        pass


string_list = [
    "id1:real;id2:↑real;proc id3;id4:real;s; proc id5;id6:real;s;id7:real$"
]

test_string = [
    "id1:real;id2:↑integer;id3:integer$",
    "id1:real;proc id2;id3:real;s$",
    "id1:↑real;proc id2;id3:integer;s$",
]


def main():
    for s in string_list:
        s.strip()
        solver = sem_relu()


    # solver.parse()


if __name__ == '__main__':
    main()

# id1:real;id2:↑integer;id3:integer$
# id1:real;proc id2;id3:real;s$
# id1:↑real;proc id2;id3:integer;s$
# id1:real;id2:↑real;proc id3;id4:real;s; proc id5;id6:real;s;id7:real$


productions = {
    'P': ['M', 'D'],
    'M': [''],
    'D': [
        ['F', 'D'],
        ['proc', 'id', ';', 'N', 'D', ';', 's'],
        ['id', ':', 'T']
    ],
    'F': [
        ['D', ';', 'F'],
        ['']
    ],
    'N': [''],
    'T': [
        ['integer'],
        ['real'],
        ['↑', 'T']
    ],
}
