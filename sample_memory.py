from circuits.components.memory import Latch
from circuits.gates import gate_and, gate_not, gate_or


def latch_test():
    latch = Latch()

    value, _ = latch(), latch.set()
    print(value)

    value, _ = latch(), latch.reset()
    print(value)


# latch_test()


class RAM:
    def __init__(self, *, multiplexer):
        self.__matrix = [[Latch()] * 4] * 4
        self.__multiplexer = multiplexer

    def plex(self, address, set=False):
        pass

    def read(self, address):
        pass

    def write(self, address, value):
        pass


def multiplexer_16x1(
    data_lines_A: list[Latch],
    data_lines_B: list[Latch],
    address: list[bool],
    *,
    set: bool = False,
    reset: bool = False,
) -> bool:
    if len(data_lines_A) != len(data_lines_B):
        return

    def plexer(data_lines, sliced_address):
        select_0, select_1, select_2, select_3 = sliced_address
        select_0_not, select_1_not, select_2_not, select_3_not = [
            gate_not(x) for x in sliced_address
        ]

        selection_lines = (
            data_lines,
            [select_0_not, select_0] * 8,
            [*[select_1_not] * 2, *[select_1] * 2] * 4,
            [*[select_2_not] * 4, *[select_2] * 4] * 2,
            [*[select_3_not] * 8, *[select_3] * 8] * 1,
        )
        selection_lines = ([*x] for x in zip(*selection_lines))

        return gate_or(gate_and(x) for x in selection_lines)

    for i, (data_line_A, data_line_B) in enumerate(zip(data_lines_A, data_lines_B)):
        plex_A, plex_B = plexer(data_line_A, address[0:4]), plexer(
            data_line_B, address[4:]
        )

        plex_crossover = gate_and((plex_A, plex_B))
        if plex_crossover:
            cell: Latch = data_line_A[i]

            if set:
                cell.set()
            elif reset:
                cell.reset()

            return cell()
    return None


data = [
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
    [
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
        Latch(),
    ],
]
data_lines_A = [[x[i] for x in data] for i in range(16)]

cell = data[0][0]
cell.set()

for row in data:
    print(row)

while True:
    print("")
    add = int(input("Enter address  : "))
    add = [int(x) for x in str(bin(add))[2:].rjust(8, "0")]
    print("Memory address :", "0b" + "".join(str(x) for x in add))
    val = multiplexer_16x1(data, data_lines_A, add, reset=True)
    print("Memory value   :", val)
