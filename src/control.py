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

from alu import (
    alu_opcode_t,
)

from opcodes import (
    opcode_t,
    is_alu_opcode,
    decode_alu_opcode,
)

class PipeLineStage(object):
    def __init__(self):
        self.value_a = data_bus(0)
        self.value_b = data_bus(0)
        self.result = data_bus(0)

def ControlUnit(
    clock,
    instruction,
    alu_opcode, operand_0, operand_1, result,
    update_select_a, update_value_a,
    update_select_b, update_value_b,
    write_enabled,
    select_a, value_a,
    select_b, value_b,
    ):

    '''
    Pipeline stages:

    0 - decode instruction
    1 - get operands
    2 - compute
    3 - store result
    '''

    pipeline = [Signal(opcode_t.add) for i in range(3)]

    operand_a = Signal(data_bus(0))
    operand_b = Signal(data_bus(0))

    @always(clock.posedge)
    def logic():
        # 0th stage
        pipeline[0].next = instruction

        # 1st stage
        pipeline[1].next = pipeline[0]
        if is_alu_opcode(instruction):
            #o, a, b, r = decode_alu_opcode(pipeline[0])
            # grml, myhdl doesn't support tuple assignment
            a = 0
            b = 1
            select_a.next = a
            select_b.next = b

        # 2nd stage
        #o, a, b, r = decode_alu_opcode(pipeline[1])
        o = alu_opcode_t.add

        pipeline[2].next = pipeline[1]
        operand_0.next = select_a
        operand_1.next = select_b
        alu_opcode.next = o

        # 3nd stage
        #o, a, b, r = decode_alu_opcode(pipeline[1])
        r = 2

        update_select_a.next = r
        update_value_a.next = result
        update_select_a.next = 31
        write_enabled.next = True

    return logic

def bench():
    pass

def test_bench():
    pass
