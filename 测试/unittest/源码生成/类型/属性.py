class C:
    @property
    def m(self):
        print(0)

    @m.setter
    def m(self, value):
        print(1)