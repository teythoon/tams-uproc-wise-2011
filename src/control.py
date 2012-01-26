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
    conditional_t,
    InstructionDecoder,
)

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
    1 - load operands
    2 - compute
    3 - store result
    '''

    # todo: find a more appropriate name for this variable
    depth = 3

    p_opcode = [Signal(opcode_t.op_nop) for i in range(depth)]
    p_conditional = [Signal(conditional_t.al) for i in range(depth)]
    p_alu_opcode = [Signal(alu_opcode_t.alu_sub) for i in range(depth)]
    p_is_alu_opcode = [Signal(False) for i in range(depth)]
    p_modify_status = [Signal(False) for i in range(depth)]
    p_argument_0 = [Signal(intbv(min = 0, max = 0xff)) for i in range(depth)]
    p_argument_1 = [Signal(intbv(min = 0, max = 0xff)) for i in range(depth)]
    p_argument_2 = [Signal(intbv(min = 0, max = 0xff)) for i in range(depth)]
    p_result = [Signal(data_bus(0)) for i in range(depth)]
    p_is_valid = [Signal(False) for i in range(depth)]

    d_instruction = Signal(data_bus(0))
    d_opcode = Signal(opcode_t.op_nop)
    d_conditional = Signal(conditional_t.al)
    d_modify_status = Signal(False)
    d_is_alu_opcode = Signal(False)
    d_alu_opcode = Signal(alu_opcode_t.alu_add)
    d_argument_0 = Signal(intbv(min = 0, max = 0xff))
    d_argument_1 = Signal(intbv(min = 0, max = 0xff))
    d_argument_2 = Signal(intbv(min = 0, max = 0xff))

    instruction_decoder = InstructionDecoder(
        d_instruction,
        d_opcode,
        d_conditional,
        d_modify_status,
        d_is_alu_opcode, d_alu_opcode,
        d_argument_0, d_argument_1, d_argument_2)

    # hack!
    once = Signal(True)

    @always(clock.posedge)
    def logic():
        # hack!
        once.next = False

        '''
        push pipeline register values
        '''
        for i in range(depth - 1):
            p_opcode[i + 1].next = p_opcode[i]
            p_alu_opcode[i + 1].next = p_alu_opcode[i]
            p_is_alu_opcode[i + 1].next = p_is_alu_opcode[i]
            p_modify_status[i + 1].next = p_modify_status[i]
            p_argument_0[i + 1].next = p_argument_0[i]
            p_argument_1[i + 1].next = p_argument_1[i]
            p_argument_2[i + 1].next = p_argument_2[i]
            p_result[i + 1].next = p_result[i]
            p_is_valid[i + 1].next = p_is_valid[i]

        '''
        0th stage - decode instruction
        '''
        d_instruction.next = instruction

        # hack!
        p_is_valid[0].next = once

        '''
        1st stage - load operands
        '''
        # note the index is 0 b/c of signal semantics!

        '''
          - remember decoding result
        '''
        p_opcode[1].next = d_opcode
        p_alu_opcode[1].next = d_alu_opcode
        p_is_alu_opcode[1].next = d_is_alu_opcode
        p_modify_status[1].next = d_modify_status
        p_argument_0[1].next = d_argument_0
        p_argument_1[1].next = d_argument_1
        p_argument_2[1].next = d_argument_2

        '''
          - load operands
        '''
        select_a.next = d_argument_0
        select_b.next = d_argument_1

        '''
        2nd stage - execute
        '''
        alu_opcode.next = p_alu_opcode[1]
        operand_0.next = value_a
        operand_1.next = value_b

        '''
        3rd stage - store result
        '''
        update_select_a.next = p_argument_2[2]
        update_value_a.next = result
        write_enabled.next = p_is_valid[2]

    return instruction_decoder, logic

def bench():
    pass

def test_bench():
    pass
