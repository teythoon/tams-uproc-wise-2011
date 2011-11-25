class Instruction(object):
    width = 8
    next_instruction = 0

    @classmethod
    def align(cls, mask):
        while cls.next_instruction & mask != 0:
            cls.next_instruction += 1
            if cls.next_instruction > 1 << cls.width:
                raise KeyError('Ran out of opcodes')

    def __init__(self, opcodes, instruction, format, (conditional, shortcut), kind, description, modifier = ''):
        # kinky ;)
        self.__dict__.update(locals())
        del self.__dict__['self']
        self.opcodes = opcodes
        self.opcode = self.next_instruction
        Instruction.next_instruction += 1

    def __str__(self):
        return '%s  %s (%s) [%s] - %s: %s' % (
            self.bin,
            self.symbol,
            self.long_format,
            self.conditional,
            self.kind,
            self.description
        )

    @property
    def long_description(self):
        return '%s%s [%s] // %s' % (
            self.description,
            self.modifier,
            self.conditional,
            self.long_format,
        )
    
    @property
    def long_format(self):
        return self.opcodes['formats'][self.format]

    def __getitem__(self, key):
        return getattr(self, key)

    @property
    def bin(self):
        return bin(self.opcode)[2:].rjust(self.width, '0')

    @property
    def mnemonic(self):
        return '%s%s %s' % (self.instruction, self.modifier, self.shortcut)

    @property
    def symbol(self):
        formats = self.opcodes['instructions'][self.kind][self.instruction][1]
        if len(formats) == 1:
            return self.instruction + self.shortcut + self.modifier
        else:
            return self.instruction + self.format + self.shortcut + self.modifie
