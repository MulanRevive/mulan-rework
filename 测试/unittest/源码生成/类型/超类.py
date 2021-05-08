class Animal:
  def __init__(self):
    print(1)

  def run(self, n):
    print(n)

class WildAnimal:
  def __init__(self, name):
    print(name)

class Person(Animal):
  def __init__(self):
    super().__init__()

  def go(self):
    super().run(3)

class Wolf(WildAnimal):
  def __init__(self):
    super().__init__(2)

Person()
Wolf()
Person().go()