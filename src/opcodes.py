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

opcode_t = enum('op_int', 'op_nop', 'op_br', 'op_call', 'op_ret', 'op_reti', 'op_drop', 'op_dropi', 'op_cmp', 'op_li', 'op_mov', 'op_add', 'op_adds', 'op_sub', 'op_subs', 'op_mul', 'op_muls', 'op_div', 'op_divs', 'op_and', 'op_ands', 'op_or', 'op_ors', 'op_xor', 'op_xors', 'op_not', 'op_nots', 'op_ld', 'op_st', 'op_pop', 'op_push')
conditional_t = enum('al', 'eq', 'ne', 'hs', 'lo', 'mi', 'pl', 'vs')
format_t = enum('r', 'rr', 'v', 'i', 'rrri', 'rrrr', 'ri')

def InstructionDecoder(instruction,
                       opcode,
                       conditional,
                       modify_status,
                       is_alu_opcode, alu_opcode,
                       argument_0, argument_1, argument_2):
    @always_comb
    def logic():
        format = format_t.r

        '''
        decode instruction
        '''
        if instruction[31:26] == 0:
            opcode.next = opcode_t.op_int
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.i
        elif instruction[31:26] == 1:
            opcode.next = opcode_t.op_nop
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.v
        elif instruction[31:26] == 2:
            opcode.next = opcode_t.op_br
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.rrri
        elif instruction[31:26] == 3:
            opcode.next = opcode_t.op_call
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.i
        elif instruction[31:26] == 4:
            opcode.next = opcode_t.op_ret
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.v
        elif instruction[31:26] == 5:
            opcode.next = opcode_t.op_reti
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.v
        elif instruction[31:26] == 6:
            opcode.next = opcode_t.op_drop
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.v
        elif instruction[31:26] == 7:
            opcode.next = opcode_t.op_dropi
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.v
        elif instruction[31:26] == 8:
            opcode.next = opcode_t.op_cmp
            modify_status.next = False
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_cmp
            format = format_t.rrri
        elif instruction[31:26] == 9:
            opcode.next = opcode_t.op_li
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.ri
        elif instruction[31:26] == 10:
            opcode.next = opcode_t.op_mov
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.rr
        elif instruction[31:26] == 12:
            opcode.next = opcode_t.op_add
            modify_status.next = False
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.rrri
        elif instruction[31:26] == 13:
            opcode.next = opcode_t.op_add
            modify_status.next = True
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.rrri
        elif instruction[31:26] == 14:
            opcode.next = opcode_t.op_sub
            modify_status.next = False
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_sub
            format = format_t.rrri
        elif instruction[31:26] == 15:
            opcode.next = opcode_t.op_sub
            modify_status.next = True
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_sub
            format = format_t.rrri
        elif instruction[31:26] == 16:
            opcode.next = opcode_t.op_mul
            modify_status.next = False
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_mul
            format = format_t.rrri
        elif instruction[31:26] == 17:
            opcode.next = opcode_t.op_mul
            modify_status.next = True
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_mul
            format = format_t.rrri
        elif instruction[31:26] == 18:
            opcode.next = opcode_t.op_div
            modify_status.next = False
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_div
            format = format_t.rrri
        elif instruction[31:26] == 19:
            opcode.next = opcode_t.op_div
            modify_status.next = True
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_div
            format = format_t.rrri
        elif instruction[31:26] == 20:
            opcode.next = opcode_t.op_and
            modify_status.next = False
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_and
            format = format_t.rrri
        elif instruction[31:26] == 21:
            opcode.next = opcode_t.op_and
            modify_status.next = True
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_and
            format = format_t.rrri
        elif instruction[31:26] == 22:
            opcode.next = opcode_t.op_or
            modify_status.next = False
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_or
            format = format_t.rrri
        elif instruction[31:26] == 23:
            opcode.next = opcode_t.op_or
            modify_status.next = True
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_or
            format = format_t.rrri
        elif instruction[31:26] == 24:
            opcode.next = opcode_t.op_xor
            modify_status.next = False
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_xor
            format = format_t.rrri
        elif instruction[31:26] == 25:
            opcode.next = opcode_t.op_xor
            modify_status.next = True
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_xor
            format = format_t.rrri
        elif instruction[31:26] == 26:
            opcode.next = opcode_t.op_not
            modify_status.next = False
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_not
            format = format_t.rr
        elif instruction[31:26] == 27:
            opcode.next = opcode_t.op_not
            modify_status.next = True
            is_alu_opcode.next = True
            alu_opcode.next = alu_opcode_t.alu_not
            format = format_t.rr
        elif instruction[31:26] == 28:
            opcode.next = opcode_t.op_ld
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.rrri
        elif instruction[31:26] == 29:
            opcode.next = opcode_t.op_st
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.rrri
        elif instruction[31:26] == 30:
            opcode.next = opcode_t.op_pop
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.rrrr
        elif instruction[31:26] == 31:
            opcode.next = opcode_t.op_push
            modify_status.next = False
            is_alu_opcode.next = False
            alu_opcode.next = alu_opcode_t.alu_add
            format = format_t.rrrr
        

        '''
        decode format
        '''
        argument_0.next = 31
        argument_1.next = 31
        argument_2.next = 31

        if format == format_t.r:
            argument_0.next = instruction[23:18]
        elif format == format_t.rr:
            argument_0.next = instruction[23:18]
            argument_1.next = instruction[18:13]

        '''
        decode conditional
        '''
        if instruction[26:23] == 0:
            conditional.next = conditional_t.al # always
        elif instruction[26:23] == 1:
            conditional.next = conditional_t.eq # equal
        elif instruction[26:23] == 2:
            conditional.next = conditional_t.ne # not equal
        elif instruction[26:23] == 3:
            conditional.next = conditional_t.hs # higher or same
        elif instruction[26:23] == 4:
            conditional.next = conditional_t.lo # lower
        elif instruction[26:23] == 5:
            conditional.next = conditional_t.mi # negative
        elif instruction[26:23] == 6:
            conditional.next = conditional_t.pl # positive
        elif instruction[26:23] == 7:
            conditional.next = conditional_t.vs # overflow
        

    return logic
