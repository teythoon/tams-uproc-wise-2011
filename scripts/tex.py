from target import Target

@Target.register
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
