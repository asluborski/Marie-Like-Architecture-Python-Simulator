from Parser import Parser


class Assembler:

    def assemble(self, op_code, address):
        parse = Parser()
        parse.parse_labels(op_code)

        PC = 0
        for line in op_code:
            commands = line.split(" ")
            parse.parse_line(commands, PC, address)
            PC += 1
