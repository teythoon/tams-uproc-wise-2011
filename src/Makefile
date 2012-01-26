.PHONY: all
all: Processor.vhd

.PHONY: Processor.vhd
Processor.vhd:
	python processor.py

opcodes.py: opcodes.yaml
	../scripts/opcodes.py myhdl "$<" "$@"

include Makefile.inc
