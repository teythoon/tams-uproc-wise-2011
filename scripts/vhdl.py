from target import Target

def bin_(n, width):
    return bin(n)[2:].rjust(width, '0')

@Target.register
class VHDL(Target):
    name = 'vhdl'

    instruction_format = 'constant op_{0.symbol: <8} : std_logic_vector(4 downto 0) := "{0.opcode_bin}";  -- {0.description: <40} - {0.symbol: <8} {0.long_format}'

    @property
    def opcode_definitions(self):
        return '\n  '.join(self.instruction_format.format(i) for i in self.opcodes)

    conditional_format = 'constant cond_{2: <2} : std_logic_vector(2 downto 0) := "{0}";  -- {1}'

    @property
    def conditional_definitions(self):
        return '\n  '.join(self.conditional_format.format(bin_(i, 3), name, shortcut or 'al')
                           for i, (name, shortcut) in enumerate(self.definitions['conditionals']))

    @property
    def opcode_enumeration(self):
        return ',\n    '.join('in_%(symbol)s' % i for i in self.opcodes)

    @property
    def conditional_enumeration(self):
        return ',\n    '.join(shortcut or 'al'
                              for (name, shortcut) in self.definitions['conditionals'])

    @property
    def format_enumeration(self):
        return ',\n    '.join(name
                              for (name, description) in self.definitions['formats'].items())

    instruction_when = r'''
        when op_{0.symbol} =>
          instruction <= in_{0.symbol};
          modify_status <= {1};
          format <= {0.format};'''

    @property
    def instruction_cases(self):
        return '\n'.join(self.instruction_when.format(instruction, "'1'" if instruction.modifier == 's' else "'0'")
                         for instruction in self.opcodes)

    conditional_when = r'''
        when cond_{0} =>
          conditional <= {0}; -- {1}'''

    @property
    def conditional_cases(self):
        return '\n'.join(self.conditional_when.format(shortcut or 'al', name)
                         for (name, shortcut) in self.definitions['conditionals'])
