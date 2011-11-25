WORKDIR      ?= work
GHDL_OPTIONS ?= --workdir="$(WORKDIR)" --warn-reserved --warn-default-binding --warn-binding --warn-error

%:
	mkdir -p work
	ghdl -i $(GHDL_OPTIONS) *vhdl
	ghdl -m $(GHDL_OPTIONS) "$@"

%.vcd: %
	ghdl -r $(GHDL_OPTIONS) "$<" --vcd="$@"

.PHONY: all
all: clean $(TARGETS)

.PHONY: test
test: $(TESTS)
	set -e ; for test in $(TESTS) ; do "$${test}" --assert-level=error ; done

.PHONY: clean
clean:
	ghdl --clean $(GHDL_OPTIONS)
	rm -rf "$(WORKDIR)" *.lst *.vcd
