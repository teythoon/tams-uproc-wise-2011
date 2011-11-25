.PHONY: all
all: architecture.pdf

opcodes.tex: ../src/opcodes.yaml
	../scripts/opcodes.py tex "$<" "$@"

architecture.pdf: opcodes.tex

%.pdf: %.tex
	rubber --ps --pdf "$<"

.PHONY: clean
clean:
	rubber --ps --pdf --clean *.tex
	rm -f opcodes.tex
