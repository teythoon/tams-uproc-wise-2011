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

from alu import ALU, alu_opcode_t
from registers import RegisterBank
from control import ControlUnit
from ram import Ram

def Processor(clock, dbus, abus):
    number_of_registers = 32

    alu_opcode = Signal(alu_opcode_t.alu_add)
    operand_0 = Signal(data_bus(0))
    operand_1 = Signal(data_bus(0))
    result = Signal(data_bus(0))

    alu = ALU(alu_opcode, operand_0, operand_1, result)

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

    opcode = Signal(data_bus(0))

    control_unit = ControlUnit(
        clock,
        opcode,
        alu_opcode, operand_0, operand_1, result,
        update_select_a, update_value_a,
        update_select_b, update_value_b,
        write_enabled,
        select_a, value_a,
        select_b, value_b,
        dbus, abus,
    )

    return alu, register_bank, control_unit

def bench(number_of_registers = 32, ram_from_file = False):

    def ClockDriver(clock, period = 100):
        @always(delay(period / 2))
        def drive_clock():
            clock.next = not clock

        return drive_clock

    clock = Signal(False)
    clock_driver = ClockDriver(clock)

    abus = Signal(data_bus(0))
    dbus = Signal(data_bus(0))
    data_in = Signal(data_bus(0))
    write_enabled = Signal(False)

    ram = Ram(
        clock,
        dbus, data_in,
        abus,
        write_enabled,
        from_file = ram_from_file,
    )

    processor = Processor(clock, dbus, abus)

    return clock_driver, ram, processor

def test_bench(ram_from_file):
    sim = Simulation(traceSignals(bench, ram_from_file = ram_from_file))
    sim.run()

if __name__ == '__main__':
    import sys

    if sys.argv[1] == 'convert':
        from myhdl import toVHDL

        clock = Signal(False)
        abus = Signal(data_bus(0))
        dbus = Signal(data_bus(0))

        toVHDL(
            Processor,
            clock,
            dbus,
            abus,
        )
    else:
        test_bench(open(sys.argv[1]))
