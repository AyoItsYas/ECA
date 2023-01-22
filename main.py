from circuits.adders import dynamic_adder
from circuits.components.memory import Latch

# latch = Latch()

# latch.set()
# print(latch())

# latch.reset()
# print(latch())

X = [int(x) for x in input("X: ")]
Y = [int(y) for y in input("X: ")]

Z, C = dynamic_adder(X, Y)
print("Z: " + ("1" if C else "") + "".join("1" if z else "0" for z in Z))
