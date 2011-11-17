%.o: %.vhdl
	ghdl -a "$<"

%: %.o
	ghdl -e "$@"

