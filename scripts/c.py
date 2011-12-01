from target import Target

@Target.register
class C(Target):
    name = 'c'

    enum_values_format = r'op_%(symbol)s = 0x%(opcode)02x'

    @property
    def enum_values(self):
        return ',\n  '.join(self.enum_values_format % i for i in self.instructions)
