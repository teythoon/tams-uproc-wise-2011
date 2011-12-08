import os
import yaml

from instruction import Instruction

def load_template(name):
    return open(os.path.join(os.path.dirname(__file__), 'templates', name)).read()

class Target(object):
    targets = dict()

    def __init__(self):
        self.instructions = list()
        self.opcode_cache = None
        self.template = load_template(self.name)

    def parse(self, handle):
        self.definitions = yaml.load(handle)

        for kind, instructions in self.definitions['instructions'].items():
            for instruction, description, formats in instructions:
                Instruction.align(0x0f if kind == 'arithmetic' else 0x07)
                if kind == 'arithmetic':
                    for modifier in ('', 's'):
                        self.create_instruction(kind, instruction, description, formats, modifier, show_format = False)
                else:
                    self.create_instruction(kind, instruction, description, formats, show_format = True)

    def create_instruction(self, kind, instruction, description, formats, modifier = '', show_format = True):
        for format_ in formats:
            for (conditional, shortcut) in self.definitions['conditionals']:
                self.instructions.append(Instruction(self.definitions, instruction, format_, (conditional, shortcut), kind, description, modifier, show_format and format_ != 'v'))

    @property
    def opcodes(self):
        if self.opcode_cache == None:
            self.opcode_cache = [instruction for instruction in self.instructions if instruction.conditional == 'always']
        return self.opcode_cache

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
