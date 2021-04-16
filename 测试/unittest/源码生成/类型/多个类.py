class C1:
    class C2:
        def __init__(self):
            print(2)

    def __init__(self):
        print(1)
C1()
C1.C2()