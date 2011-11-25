import os
import yaml

from instruction import Instruction

def load_template(name):
    return open(os.path.join(os.path.dirname(__file__), 'templates', name)).read()

class Target(object):
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
        return dict(
            vhdl = VHDL,
            tex = Tex,
            c = C,
        )[target](*args, **kwargs)

class VHDL(Target):
    name = 'vhdl'

    instruction_format = 'constant op_%(symbol)s : std_logic_vector(word_width - 1 downto 0) := "%(bin)s";  -- %(long_description)s'

    @property
    def opcode_definitions(self):
        return '\n  '.join(self.instruction_format % i for i in self.instructions)

    @property
    def opcode_enumeration(self):
        return ',\n    '.join('%(symbol)s' % i for i in self.instructions)

class Tex(Target):
    name = 'tex'

    table_row_format = r'%(mnemonic)s & %(conditional)s & %(long_format)s & %(bin)s \\'

    @property
    def table_rows(self):
        rows = []
        
        lastinstruction = None
        for i in self.instructions:
            if lastinstruction != None and lastinstruction != i.instruction:
                rows.append('\hline')
            lastinstruction = i.instruction
            rows.append(self.escape(self.table_row_format % i))

        return '\n    '.join(rows)
    
    def escape(self, s):
        return s.replace('<', '\(\langle\)')

class C(Target):
    name = 'c'

    enum_values_format = r'op_%(symbol)s = 0x%(opcode)02x'

    @property
    def enum_values(self):
        return ',\n  '.join(self.enum_values_format % i for i in self.instructions)
