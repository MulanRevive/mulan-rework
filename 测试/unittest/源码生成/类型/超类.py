class Animal:
  def __init__(self):
    self.name = 1

class WildAnimal:
  def __init__(self, name):
    self.name = name

class Person(Animal):
  def __init__(self):
    super().__init__()

class Wolf(WildAnimal):
  def __init__(self):
    super().__init__(2)

print(Person().name)
print(Wolf().name)