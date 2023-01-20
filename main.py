from circuits.components.memory import Latch

latch = Latch()

latch.set()
print(latch())

latch.reset()
print(latch())
