from circuits import components
from circuits import utils


log = utils.Logger()
logger = lambda *x, **y: log.log("mem-test", *x, **y, origin=__name__)


dbus = components.Bus(8)
abus = components.Bus(5)

mem = components.memory.Memory(dbus, abus, logger=log.get_logger("mem"))

mem.decode_hook()

for i, row in enumerate(mem._Memory__memory_matrix):
    logger(str(i) + " " + str(row))

logger(mem._Memory__address_lines.read())
logger(mem._Memory__data_lines.read())

dbus.write([1, 1, 1, 0, 1, 1, 1, 0])
abus.write((1, 1, 1, 1, 1))

logger(mem._Memory__address_lines.read())
logger(mem._Memory__data_lines.read())


mem.decode_hook()

for i, row in enumerate(mem._Memory__memory_matrix):
    logger(str(i) + " " + str(row))
