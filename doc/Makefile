TARGETS = architecture.pdf
DEPLOY_PATH ?= publisher:public_html/tams-uproc-wise-2011

.PHONY: all
all: $(TARGETS)

.PHONY: deploy
deploy: $(TARGETS)
	rsync -av $(TARGETS) $(DEPLOY_PATH)

opcodes.tex: ../src/opcodes.yaml
	../scripts/opcodes.py tex "$<" "$@"

architecture.pdf: opcodes.tex isa.tex abi.tex

%.pdf: %.tex
	rubber --ps --pdf "$<"

.PHONY: clean
clean:
	rubber --ps --pdf --clean *.tex
	rm -f opcodes.tex
