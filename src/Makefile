TARGETS = processor
TESTS = alu_tb registers_tb

processor: instructions.vhdl

instructions.vhdl: opcodes.yaml
	../scripts/opcodes.py vhdl "$<" "$@"

include Makefile.inc
