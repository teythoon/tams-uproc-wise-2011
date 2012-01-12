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
    opcode_t,
)

from alu import ALU
from registers import RegisterBank

def Processor(clock):
    number_of_registers = 32

    opcode = Signal(opcode_t.add)
    operand_0 = Signal(data_bus(0))
    operand_1 = Signal(data_bus(0))
    result = Signal(data_bus(0))

    alu = ALU(opcode, operand_0, operand_1, result)

    update_select_a = Signal(intbv(min = 0, max = number_of_registers))
    update_value_a = Signal(data_bus(0))
    update_select_b = Signal(intbv(min = 0, max = number_of_registers))
    update_value_b = Signal(data_bus(0))
    write_enabled = Signal(False)

    select_a = Signal(intbv(min = 0, max = number_of_registers))
    value_a = Signal(data_bus(0))
    select_b = Signal(intbv(min = 0, max = number_of_registers))
    value_b = Signal(data_bus(0))

    register_bank = RegisterBank(
        update_select_a, update_value_a,
        update_select_b, update_value_b,
        write_enabled,
        select_a, value_a,
        select_b, value_b,
        clock,
    )

    @always(clock.posedge)
    def logic():
        opcode.next = opcode_t.add
        operand_0.next = 1
        operand_1.next = 1

        update_select_a.next = 0
        update_value_a.next = 0
        update_select_b.next = 0
        update_value_b.next = 0
        write_enabled.next = False
        select_a.next = 0
        select_b.next = 0

    return alu, register_bank, logic

if __name__ == '__main__':
    from myhdl import toVHDL

    clock = Signal(False)

    toVHDL(
        Processor,
        clock,
    )
