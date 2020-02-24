class C:
    count = 0

    def __init__(self, a):
        self.count += 1
        self.a = a


ins = [C(i) for i in range(10)]
print(C.count)

