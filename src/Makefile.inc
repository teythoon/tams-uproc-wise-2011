WORKDIR      ?= work
GHDL_OPTIONS ?= --workdir="$(WORKDIR)" --warn-reserved --warn-default-binding --warn-binding --warn-error

%.o: %.vhdl
	mkdir -p work
	ghdl -i $(GHDL_OPTIONS) *vhdl
	ghdl -a $(GHDL_OPTIONS) "$<"

%: %.o
	ghdl -e $(GHDL_OPTIONS) "$@"

%.vcd: %
	ghdl -r $(GHDL_OPTIONS) "$<" --vcd="$@"

.PHONY: all
all: clean $(TARGETS)

.PHONY: test
test: all $(TESTS)
	set -e ; for test in ./*_tb ; do "$${test}" --assert-level=error ; done

.PHONY: clean
clean:
	ghdl --clean $(GHDL_OPTIONS)
	rm -rf "$(WORKDIR)" *.lst *.vcd
