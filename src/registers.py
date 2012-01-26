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

PROGRAM_COUNTER = 30
ZERO_REGISTER = 31

def RegisterBank(
    update_select_a, update_value_a,
    update_select_b, update_value_b,
    write_enabled,
    select_a, value_a,
    select_b, value_b,
    instruction_register, update_instruction_register, write_instruction_register,
    clock,
    number_of_registers = 32):

    '''
    Comment
    '''

    registers = [Signal(data_bus(0)) for i in range(number_of_registers)]

    @always_comb
    def read_logic():
        '''
        Handles reads to the register bank.
        '''
        value_a.next = registers[select_a]
        value_b.next = registers[select_b]
        instruction_register.next = registers[PROGRAM_COUNTER]

    @always(clock.posedge)
    def logic():
        '''
        Updates the values stored in the register bank.
        '''
        if write_enabled:
            registers[update_select_a].next = update_value_a
            registers[update_select_b].next = update_value_b

        if write_instruction_register:
            registers[PROGRAM_COUNTER].next = update_instruction_register

    return logic, read_logic

def bench(number_of_registers = 32):
    update_select_a = Signal(intbv(min = 0, max = number_of_registers))
    update_value_a = Signal(data_bus(0))
    update_select_b = Signal(intbv(min = 0, max = number_of_registers))
    update_value_b = Signal(data_bus(0))
    write_enabled = Signal(False)

    select_a = Signal(intbv(min = 0, max = number_of_registers))
    result_a = Signal(data_bus(0))
    select_b = Signal(intbv(min = 0, max = number_of_registers))
    result_b = Signal(data_bus(0))

    instruction_register = Signal(data_bus(0))
    update_instruction_register = Signal(data_bus(0))
    write_instruction_register = Signal(False)

    clock = Signal(False)

    register_bank = RegisterBank(
        update_select_a, update_value_a,
        update_select_b, update_value_b,
        write_enabled,
        select_a, result_a,
        select_b, result_b,
        instruction_register, update_instruction_register, write_instruction_register,
        clock,
        number_of_registers,
    )

    @instance
    def stimulus():
        for i in range(number_of_registers):
            for v in range(100):
                update_select_a.next = i
                update_value_a.next = v
                update_select_b.next = i
                update_value_b.next = v
                write_enabled.next = True

                clock.next = True
                yield delay(10)
                clock.next = False
                yield delay(10)

                write_enabled.next = False
                select_a.next = i
                select_b.next = i

                clock.next = True
                yield delay(10)
                clock.next = False
                yield delay(10)

                assert result.signed() == v

    return register_bank, stimulus

def test_bench():
    sim = Simulation(traceSignals(bench))
    sim.run()

if __name__ == '__main__':
    from myhdl import toVHDL

    number_of_registers = 32

    update_select_a = Signal(intbv(min = 0, max = number_of_registers))
    update_value_a = Signal(data_bus(0))
    update_select_b = Signal(intbv(min = 0, max = number_of_registers))
    update_value_b = Signal(data_bus(0))
    write_enabled = Signal(False)

    select_a = Signal(intbv(min = 0, max = number_of_registers))
    result_a = Signal(data_bus(0))
    select_b = Signal(intbv(min = 0, max = number_of_registers))
    result_b = Signal(data_bus(0))

    clock = Signal(False)

    toVHDL(
        RegisterBank,
        update_select_a, update_value_a,
        update_select_b, update_value_b,
        write_enabled,
        select_a, result_a,
        select_b, result_b,
        clock,
        number_of_registers,
    )
