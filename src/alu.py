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

from common import (
    data_bus,
)

alu_opcode_t = enum('alu_add', 'alu_sub', 'alu_mul', 'alu_div',
                    'alu_and', 'alu_or', 'alu_xor', 'alu_not',
                    'alu_cmp',)

def ALU(opcode, operand_0, operand_1, result):
    @always_comb
    def logic():
        if opcode == alu_opcode_t.alu_add:
            result.next = operand_0 + operand_1
        elif opcode == alu_opcode_t.alu_sub:
            result.next = operand_0 - operand_1
        elif opcode == alu_opcode_t.alu_mul:
            result.next = operand_0 * operand_1
        elif opcode == alu_opcode_t.alu_div:
            result.next = operand_0 // operand_1
        elif opcode == alu_opcode_t.alu_and:
            result.next = operand_0 & operand_1
        elif opcode == alu_opcode_t.alu_or:
            result.next = operand_0 | operand_1
        elif opcode == alu_opcode_t.alu_xor:
            result.next = operand_0 ^ operand_1
        elif opcode == alu_opcode_t.alu_not:
            result.next = not operand_0
        elif opcode == alu_opcode_t.alu_cmp:
            # todo: fix cmp
            result.next = operand_0 < operand_1

    return logic

def bench():
    opcode = Signal(alu_opcode_t.alu_add)
    operand_0 = Signal(data_bus(0))
    operand_1 = Signal(data_bus(0))
    result = Signal(data_bus(0))

    alu = ALU(opcode, operand_0, operand_1, result)

    @instance
    def stimulus():
        for i in range(100):
            for operator, compute_result in (
                (alu_opcode_t.alu_add, lambda a, b: a + b),
                (alu_opcode_t.alu_sub, lambda a, b: a - b),
                ):
                a = random.randrange(-2 ** 30, 2 ** 30)
                b = random.randrange(-2 ** 30, 2 ** 30)
                expect = compute_result(a, b)

                opcode.next = operator
                operand_0.next = data_bus(a)
                operand_1.next = data_bus(b)

                yield delay(10)

                assert result.signed() == expect

    return alu, stimulus

def test_bench():
    sim = Simulation(traceSignals(bench))
    sim.run()

if __name__ == '__main__':
    from myhdl import toVHDL

    opcode = Signal(alu_opcode_t.alu_add)
    operand_0 = Signal(data_bus(0))
    operand_1 = Signal(data_bus(0))
    result = Signal(data_bus(0))

    toVHDL(ALU, opcode, operand_0, operand_1, result)
