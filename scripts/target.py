import os
import yaml

from instruction import Instruction

def load_template(name):
    return open(os.path.join(os.path.dirname(__file__), 'templates', name)).read()

class Target(object):
    targets = dict()

    def __init__(self):
        self.instructions = list()
        self.template = load_template(self.name)

    def parse(self, handle):
        opcodes = yaml.load(handle)

        for kind, instructions in opcodes['instructions'].items():
            for instruction, description, formats in instructions:
                Instruction.align(0x0f if kind == 'arithmetic' else 0x07)
                if kind == 'arithmetic':
                    for modifier in ('', 's'):
                        self.create_instruction(opcodes, kind, instruction, description, formats, modifier, show_format = False)
                else:
                    self.create_instruction(opcodes, kind, instruction, description, formats, show_format = True)

    def create_instruction(self, opcodes, kind, instruction, description, formats, modifier = '', show_format = True):
        for format_ in formats:
            for (conditional, shortcut) in opcodes['conditionals']:
                self.instructions.append(Instruction(opcodes, instruction, format_, (conditional, shortcut), kind, description, modifier, show_format and format_ != 'v'))

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return self.template % self

    @classmethod
    def make(cls, target, *args, **kwargs):
        return cls.targets[target](*args, **kwargs)

    @classmethod
    def register(cls, target):
        cls.targets[target.__name__.lower()] = target
        return target
