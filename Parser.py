def remove_empty(label):
    label = filter(None, label)


class Parser:

    def __init__(self):
        self.InstructionSet = {"HALT": 0,
                         "ADD": 1,
                         "SUBT": 2,
                         "STORE": 3,
                         "LOAD": 5,
                         "BALW": 6,
                         "BIZ": 7,
                         "BIG": 8,
                         "INPUT": 9,
                         "OUTPUT": 9,
                         "VAR": 4}
        self.labels = dict()

    def parse_labels(self, lineNum):
        step = 0
        for line in lineNum:
            labels = line.split(" ")
            remove_empty(labels)
            if not labels[0] in self.InstructionSet:
                self.labels[labels[0]] = step  # insert label
            step += 1

    def fetchNextInstruction(self, memory, op_code, ref_address, mem_location):
        memory_address = 0
        try:
            memory_address = int(ref_address)
        except ValueError:
            memory_address = self.labels[ref_address]
        memory[mem_location] = int(str(op_code) + str(memory_address))

    def parse_line(self, line, memptr, address):
        remove_empty(line)
        op_code = line[0]
        if op_code == "INPUT":
            self.fetchNextInstruction(address, 9, "01", memptr)
        elif op_code == "OUTPUT":
            self.fetchNextInstruction(address, 9, "02", memptr)
        elif op_code == "HALT":
            self.fetchNextInstruction(address, 0, "00", memptr)
        else:
            if op_code in self.InstructionSet:
                self.fetchNextInstruction(
                    address, self.InstructionSet[op_code], line[1], memptr)
            else:
                if line[1] == "VAR":
                    if len(line) == 2:
                        address[memptr] = 0
                    else:
                        address[memptr] = int(line[2])
                else:
                    line.pop(0)
                    self.parse_line(line, memptr, address)

    def assemble(self, command_list, memory):
        self.parse_labels(command_list)

        instruction_ptr = 0
        for line in command_list:
            commands = line.split(" ")
            self.parse_line(commands, instruction_ptr, memory)
            instruction_ptr += 1
