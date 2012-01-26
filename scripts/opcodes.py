#!/usr/bin/env python

import sys

from target import Target
import vhdl
import tex
import c
import myhdl

def usage(message = None):
    if message != None:
        sys.stderr.write('%s\n' % message)
    sys.exit("Usage: %s (%s) opcode_file [write_to]" % (sys.argv[0], '|'.join(Target.targets.keys())))

if len(sys.argv) == 3:
    format_, opcode_file = sys.argv[1:]
    write_to = '-'
elif len(sys.argv) == 4:
    format_, opcode_file, write_to = sys.argv[1:]
else:
    usage('Wrong number of arguments')

if format_ not in Target.targets:
    usage('Unknown format %r' % format_)

target = Target.make(format_)
target.parse(open(opcode_file))

result_handle = open(write_to, 'w') if write_to != '-' else sys.stdout
result_handle.write(str(target))
