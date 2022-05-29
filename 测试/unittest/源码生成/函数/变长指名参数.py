def a(**kwargs):
    print(kwargs)

def b(*args):
    print(args)

a(k1="v1", k2="v2")
b(3, 4)
