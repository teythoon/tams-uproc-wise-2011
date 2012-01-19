from __future__ import print_function

from myhdl import (
    enum,
    intbv,

    Simulation,
    Signal,

    bin,
    traceSignals,

    delay,
    instance,
    always_comb,
)

from common import (
    data_bus,
)

from alu import (
    alu_opcode_t,
)

opcode_t = enum('add', 'sub', 'div', 'mul')

def is_alu_opcode(instruction):
    return True

def decode_alu_opcode(instruction):
    return alu_opcode_t.add, 0, 1, 2
