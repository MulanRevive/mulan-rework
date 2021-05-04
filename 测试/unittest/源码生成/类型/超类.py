class Animal:
  def __init__(self):
    self.name = 'animal'

class WildAnimal:
  def __init__(self, name):
    self.name = name

class Person(Animal):
  def __init__(self):
    super().__init__()

class Wolf(WildAnimal):
  def __init__(self):
    super().__init__("wowo")

print(Person().name)
print(Wolf().name)