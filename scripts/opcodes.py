#!/usr/bin/env python

import sys
import os
import ast
import yaml

import pprint

def usage(message = None):
    if message != None:
        sys.stderr.write('%s\n' % message)
    sys.exit("Usage: %s (vhdl|tex) opcode_file [write_to]" % sys.argv[0])

from instruction import Instruction
from target import Target

if len(sys.argv) == 3:
    format_, opcode_file = sys.argv[1:]
    write_to = '-'
elif len(sys.argv) == 4:
    format_, opcode_file, write_to = sys.argv[1:]
else:
    usage('Wrong number of arguments')

if format_ not in ('vhdl', 'tex'):
    usage('Unknown format %r' % format_)


target = Target.make(format_)
target.parse(open(opcode_file))

result_handle = open(write_to, 'w') if write_to != '-' else sys.stdout
result_handle.write(str(target))
