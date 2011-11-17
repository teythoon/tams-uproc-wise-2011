%.o: %.vhdl
	ghdl -a "$<"

%: %.o
	ghdl -e "$@"

%.vcd: %
	ghdl -r "$<" --vcd="$@"

.PHONY: all
all: clean $(TARGETS)

.PHONY: test
test: all $(TESTS)
	set -e ; for test in ./*_tb ; do "$${test}" ; done

.PHONY: clean
clean:
	rm -f $(TARGETS) $(TESTS) *.o *.cf *.vcd
