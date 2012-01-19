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
    always,
    always_comb,
)

from common import (
    data_bus,
)

def Ram(clock, data_out, data_in, address, write_enabled, number_of_ram=128):

    mem = [Signal(intbv(0)[32:]) for i in range(number_of_ram)]

    @always(clock.posedge)
    def write():
        if write_enabled:
            mem[address].next = data_in

    @always_comb
    def read():
        data_out.next = mem[address]

    return write, read

if __name__ == '__main__':
    from myhdl import toVHDL

    number_of_ram=128

    addressess = Signal(intbv(min = 0, max = number_of_ram))
    data_in = Signal(data_bus(0))
    data_out = Signal(data_bus(0))
    write_enabled = Signal(False)
    clock = Signal(False)

    toVHDL(
        Ram,
        data_in, data_out,
        addressess,
        write_enabled,
        clock,
        number_of_ram,
    )

