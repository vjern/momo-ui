


class A:
    def __and__(self, other):
        return other.__name__


print(A() &float)