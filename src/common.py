from __future__ import print_function

import random

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

opcode_t = enum('add', 'sub', 'mul', 'div')

def data_bus(value, width = 32):
    return intbv(
        value,
        min = -(2 ** (width - 1)),
        max = 2 ** (width - 1),
    )
