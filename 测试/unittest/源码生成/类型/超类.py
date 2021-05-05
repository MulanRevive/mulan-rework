class Animal:
  def __init__(self):
    print(1)

class WildAnimal:
  def __init__(self, name):
    print(name)

class Person(Animal):
  def __init__(self):
    super().__init__()

class Wolf(WildAnimal):
  def __init__(self):
    super().__init__(2)

Person()
Wolf()