

class Foo:
    def __init__(self, id):
        self.id = id
        self.data = 777

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return 'Foo id = {}, data = {}\n'.format(self.id, self.data)


def test0():
    s = set()
    d = {}

    f1 = Foo(0)
    f2 = Foo(7788899)
    f3 = Foo(-1)

    s.add(f1)
    s.add(f2)

    d[f1] = f1
    d[f2] = f2

    print(f2 in s)
    print(f3 in s)

    print(f2 in d)
    print(f3 in d)

    d2 = {f: f for f in [f1, f2]}
    print(d2[f2])
    print(d2[f1])

    print('OK')


def test1():
    f1 = Foo(0)
    f2 = Foo(789)

    d = vars(f1)
    d['id'] = -1

    print(f1)


def test2():
    f = Foo(123)

    fields = vars(f)

    print(f)
    print(fields)

    for k in fields.keys():
        fields[k] += 1

    print(f)


if __name__ == '__main__':
    # test0()
    # test1()
    test2()
