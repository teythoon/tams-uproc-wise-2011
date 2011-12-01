from target import Target

@Target.register
class VHDL(Target):
    name = 'vhdl'

    instruction_format = 'constant op_%(symbol)s : std_logic_vector(word_width - 1 downto 0) := "%(bin)s";  -- %(long_description)s'

    @property
    def opcode_definitions(self):
        return '\n  '.join(self.instruction_format % i for i in self.instructions)

    @property
    def opcode_enumeration(self):
        return ',\n    '.join('%(symbol)s' % i for i in self.instructions)
