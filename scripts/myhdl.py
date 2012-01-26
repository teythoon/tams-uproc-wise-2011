from target import Target

@Target.register
class MyHDL(Target):
    name = 'myhdl'

    @property
    def opcode_enumeration(self):
        return ', '.join("'op_%s%s'" % (i.instruction, i.modifier) for i in self.opcodes)

    @property
    def conditional_enumeration(self):
        return ', '.join(repr(shortcut or 'al')
                         for (name, shortcut) in self.definitions['conditionals'])

    @property
    def format_enumeration(self):
        return ', '.join(repr(name)
                         for (name, description) in self.definitions['formats'].items())

    instruction_when = r'''if instruction[32:27] == {0.opcode_int}:
            opcode.next = opcode_t.op_{0.instruction}
            modify_status.next = {1}
            is_alu_opcode.next = {2}
            alu_opcode.next = {3}
            format = format_t.{0.format}
        '''

    @property
    def decode_instruction(self):
        return 'el'.join(
            self.instruction_when.format(
                instruction,
                instruction.modifier == 's',
                instruction.kind in ('arithmetic', 'comparison'),
                'alu_opcode_t.alu_%s' % instruction.instruction if instruction.kind in ('arithmetic', 'comparison') else 'alu_opcode_t.alu_add',
                )
            for instruction in self.opcodes)

    conditional_when = r'''if instruction[27:24] == {0}:
            conditional.next = conditional_t.{1} # {2}
        '''

    @property
    def decode_conditional(self):
        return 'el'.join(
            self.conditional_when.format(n, shortcut or 'al', name)
            for n, (name, shortcut) in enumerate(self.definitions['conditionals']))
