from tkinter import *
from Parser import Parser


class MainFrame(Frame):

    # constructor

    def __init__(self, master=None):
        Frame.__init__(self, master)
        Frame.grid_columnconfigure(self, 3, minsize=20)
        self.master = master
        self.reset_machine()
        self.show_mainframe()
        self.update_memoryTable()
        self.update_CPUState()

    def load(self):
        self.reset_machine()

        instructionList = self.textarea.get(1.0, END)
        instructionList.upper()
        instructionList = instructionList.split("\n")
        instructionList.pop(len(instructionList) - 1)
        assembler = Parser()
        assembler.assemble(instructionList, self.memory)
        self.update_memoryTable()

    def run(self):

        def Add():
            self.accumulator += self.memory[self.address_register]

        def Sub():
            self.accumulator -= self.memory[self.address_register]

        def Load():
            self.accumulator = self.memory[self.address_register]

        def Store():
            self.memory[self.address_register] = self.accumulator

        def BranchAlways():
            self.program_counter = self.address_register

        def BranchIfZero():
            if self.accumulator == 0:
                BranchAlways()

        def BranchIfZeroOrPositive():
            if self.accumulator >= 0:
                BranchAlways()

        def lmcOutput():
            self.update_output()

        def lmcIO():
            if self.address_register == 1:
                lmcInput()
            elif self.address_register == 2:
                lmcOutput()

        def lmcInput():
            self.var = IntVar()
            self.inputarea = Text(self, height=1, width=5)
            self.inputbutton = Button(
                self, text="Confirm", command=lambda: self.var.set(1))
            self.inputarea.grid(row=16, column=4)
            self.inputbutton.grid(row=16, column=5)

            self.inputbutton.wait_variable(self.var)
            self.tempvar = self.inputarea.get(1.0, END)
            self.accumulator = int(self.tempvar)
            self.inputarea.delete(1.0, END)
            self.update_CPUState()
            self.update_memoryTable()

        instruction_list = [
            Add,  # 1
            Sub,  # 2
            Store,  # 3
            IO,  # 4
            Load,  # 5
            BranchAlways,  # 6
            BranchIfZero,  # 7
            BranchIfZeroOrPositive,  # 8
            IO]  # 8

        while self.instruction_register != 0:

            instr = str(self.memory[self.program_counter])
            if int(instr) == 0:
                break
            opcode = instr[0]

            if len(instr) == 3:
                address = instr[1] + instr[2]
            else:
                address = instr[1]

            self.program_counter += 1

            self.instruction_register = int(opcode)
            self.address_register = int(address)

            instruction_list[self.instruction_register - 1]()



    def show_mainframe(self):
        self.master.title("MarPy")
        self.pack(fill=BOTH, expand=1)
        self.header_label = Label(self, text="Text Editor")
        self.header_label.grid(row=0, column=0, columnspan=3)
        self.textarea = Text(self, width=40, height=35, font=("Helvetica", 14))
        self.textarea.grid(row=1, column=0, columnspan=3, rowspan=20)

        self.execute_button = Button(self, text="Execute", command=self.run)
        self.execute_button.grid(row=22, column=0)
        self.reset_button = Button(self, text="Reset", command=self.resetTextArea)
        self.reset_button.grid(row=22, column=1)
        self.burn_it_all = Button(self, text="Exit", command=self.exit)
        self.burn_it_all.grid(row=22, column=2)
        self.assemble = Button(
            self, text="Assemble", command=self.load)
        self.assemble.grid(row=23, column=0)

    def update_CPUState(self):
        self.cpustate_label = Label(self, text="CPU State", font=("Helvetica", 12, 'bold'))
        self.cpustate_label.grid(row=0, column=4)
        self.accvar = IntVar()
        self.accvarHex = IntVar()
        self.accvar.set(self.accumulator)
        self.accvarHex.set(hex(self.accumulator))
        self.accumulator_label = Label(self, text="Accumulator")
        self.accumulator_label.grid(row=1, column=4)
        self.accumulator_value = Label(
            self, textvariable=self.accvar, bg='grey')
        self.accumulator_value.grid(row=2, column=4)
        self.accumulator_valueHex = Label(
            self, textvariable=self.accvarHex, bg='grey')
        self.accumulator_valueHex.grid(row=3, column=4)

        self.progvar = IntVar()
        self.progvarHex = IntVar()
        self.progvar.set(self.program_counter)
        self.progvarHex.set(hex(self.program_counter))
        self.prog_label = Label(self, text="MAR")
        self.prog_label.grid(row=4, column=4)
        self.prog_value = Label(self, textvariable=self.progvar, bg='grey')
        self.prog_value.grid(row=5, column=4)
        self.prog_valueHex = Label(self, textvariable=self.progvarHex, bg='grey')
        self.prog_valueHex.grid(row=6, column=4)

        self.addressvar = IntVar()
        self.addressvar.set(self.address_register)
        self.address_label = Label(self, text="Current Address")
        self.address_label.grid(row=7, column=4)
        self.address_value = Label(
            self, textvariable=self.addressvar, bg='grey')
        self.address_value.grid(row=8, column=4)

        self.instruction_value = IntVar()
        self.instruction_value.set(self.instruction_register)
        self.instruction_label = Label(self, text="Instruction Register")
        self.instruction_label.grid(row=10, column=4)
        self.instruction_value = Label(
            self, textvariable=self.instruction_value, bg='grey')
        self.instruction_value.grid(row=11, column=4)

        self.memorytable_label = Label(self, text="Memory Table", font=("Helvetica", 18, 'bold'))
        self.memorytable_label.grid(row=17, column=94)

    def update_output(self):
        self.output_value = IntVar()
        self.output_value.set(self.accumulator)
        self.output_label = Label(self, text="Output")
        self.output_label.grid(row=13, column=4)
        self.output_value = Label(
            self, textvariable=self.output_value, bg='grey')
        self.output_value.grid(row=14, column=4)
        self.update_CPUState()

    def update_memoryTable(self):

        for x in range(0, 10):
            for y in range(0, 20):
                var = StringVar()
                value_var = StringVar()
                if y % 2 == 0:
                    loc_var = int((y / 2) * 10 + x)
                    var.set("+" + str(loc_var))
                    self.memory_label = Label(self, textvariable=var)
                    self.memory_label.grid(
                        row=18 + (y), column=90 + (x), ipadx=80, ipady=10)
                else:
                    value_var.set(self.memory[loc_var])
                    self.memory_value = Label(
                        self, textvariable=value_var, fg="green", bg='black')
                    self.memory_value.grid(row=18 + (y), column=90 + (x))

    def resetTextArea(self):
        self.textarea.delete(1.0, END)
        self.reset_machine()

    def reset_machine(self):
        self.memory = []
        self.program_counter = 0
        self.instruction_register = -1
        self.address_register = 0
        self.accumulator = 0
        for i in range(100):
            self.memory.append(0)
        self.update_CPUState()
        self.update_memoryTable()
        self.update_output()

    def exit(self):
        exit()


def main():
    root = Tk()
    root.geometry("2560x1440")
    app = MainFrame(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
