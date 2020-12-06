import os
from collections import deque
from datetime import time
from tkinter import *
from tkinter import filedialog

from Assembler import Assembler


class MainFrame(Frame):
    pipelinelist = []

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
        assembler = Assembler()
        assembler.assemble(instructionList, self.memory)
        self.update_memoryTable()

    def run(self):

        def Add():
            self.accumulator += self.memory[self.MAR]

        def Sub():
            self.accumulator -= self.memory[self.MAR]

        def Load():
            self.accumulator = self.memory[self.MAR]

        def Store():
            self.memory[self.MAR] = self.accumulator

        def JUMP():
            self.PC = self.MAR

        def BranchIfZero():
            if self.accumulator == 0:
                JUMP()

        def BranchIfZeroOrPositive():
            if self.accumulator >= 0:
                JUMP()

        def Output():
            self.update_output()

        def IO():
            if self.MAR == 1:
                Input()
            elif self.MAR == 2:
                Output()

        def Input():
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
            JUMP,  # 6
            BranchIfZero,  # 7
            BranchIfZeroOrPositive,  # 8
            IO]  # 8

        # FETCH MEMORY
        while self.IR != 0:

            instr = str(self.memory[self.PC])
            if int(instr) == 0:
                break
            opcode = instr[0]

            if len(instr) == 3:
                address = instr[1] + instr[2]
            else:
                address = instr[1]

            self.PC += 1

            self.IR = int(opcode)
            self.MAR = int(address)

            instruction_list[self.IR - 1]()

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
        self.IOButton = Button(
            self, text="Load File", command=lambda: self.load_file(self.textarea))
        self.IOButton.grid(row=23, column=1)
        self.showPipeline = Button(self, text="Show Pipeline", command=self. iterate_linesRest).grid(column=1, row=24)

        self.SaveButton = Button(
            self, text="Save File", command=lambda: self.save_file(self.textarea))
        self.SaveButton.grid(row=23, column=2)

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
            self, textvariable=self.accvar, fg="white", bg='black')
        self.accumulator_value.grid(row=2, column=4)
        self.accumulator_valueHex = Label(
            self, textvariable=self.accvarHex,  fg="white",bg='black')
        self.accumulator_valueHex.grid(row=3, column=4)

        self.progvar = IntVar()
        self.progvarHex = IntVar()
        self.progvar.set(self.PC)
        self.progvarHex.set(hex(self.PC))
        self.prog_label = Label(self, text="MAR")
        self.prog_label.grid(row=4, column=4)
        self.prog_value = Label(self, textvariable=self.progvar, fg="white", bg='black')
        self.prog_value.grid(row=5, column=4)
        self.prog_valueHex = Label(self, textvariable=self.progvarHex, fg="white", bg='black')
        self.prog_valueHex.grid(row=6, column=4)

        self.PCVar = IntVar()
        self.PCVarHex = IntVar()
        self.PCVar.set(self.PC)
        self.PCVarHex.set(hex(self.PC))
        self.PC_Label = Label(self, text="PC")
        self.PC_Label.grid(row=1, column=5)
        self.PCVar = Label(self, textvariable=self.PCVar, fg="white", bg='black')
        self.PCVar.grid(row=2, column=5)
        self.PCVarHex = Label(self, textvariable=self.PCVarHex,  fg="white", bg='black')
        self.PCVarHex.grid(row=3, column=5)

        self.addressvar = IntVar()
        self.addressvarHex = IntVar()
        self.addressvar.set(self.MAR)
        self.addressvarHex.set(hex(self.MAR))
        self.address_label = Label(self, text="MBR")
        self.address_label.grid(row=7, column=4)
        self.address_value = Label(
            self, textvariable=self.addressvar, fg="white", bg='black')
        self.address_value.grid(row=8, column=4)
        self.address_valueHex = Label(
            self, textvariable=self.addressvarHex, fg="white", bg='black')
        self.address_valueHex.grid(row=9, column=4)

        self.instruction_value = IntVar()
        self.instruction_valueHex = IntVar()
        self.instruction_value.set(self.IR)
        self.instruction_valueHex.set(hex(self.IR))
        self.instruction_label = Label(self, text="Instruction Register")
        self.instruction_label.grid(row=10, column=4)
        self.instruction_value = Label(
            self, textvariable=self.instruction_value, fg="white", bg='black')
        self.instruction_value.grid(row=11, column=4)
        self.instruction_valueHex = Label(
            self, textvariable=self.instruction_valueHex,  fg="white", bg='black')
        self.instruction_valueHex.grid(row=12, column=4)


        self.memorytable_label = Label(self, text="Memory Table", font=("Helvetica", 18, 'bold'))
        self.memorytable_label.grid(row=17, column=94)

    def update_output(self):
        self.output_value = IntVar()
        self.output_value2 = IntVar()
        self.output_value.set(self.accumulator)
        self.output_value2.set(hex(self.accumulator))
        self.output_label = Label(self, text="Output")
        self.output_label.grid(row=13, column=4)
        self.output_value = Label(
            self, textvariable=self.output_value, fg="white", bg='black')
        self.output_value.grid(row=14, column=4)
        self.output_value2 = Label(
            self, textvariable=self.output_value2, fg="white", bg='black')
        self.output_value2.grid(row=15, column=4)

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
                        self, textvariable=value_var, fg="white", bg='black')
                    self.memory_value.grid(row=18 + (y), column=90 + (x))
        self.pipeline_label = Label(self, text="3 Stage Pipeline", font=("Helvetica", 16, 'bold'))
        self.pipeline_label.grid(row=1, column=94)
        self.fetch_label = Label(
            self, text="Fetch:", font=("Helvetica", 10, 'bold'))
        self.fetch_label.grid(row=2, column=93)
        self.decode_label = Label(
            self, text="Decode:", font=("Helvetica", 10, 'bold'))
        self.decode_label.grid(row=2, column=94)
        self.execute_label = Label(
            self, text="Execute:", font=("Helvetica", 10, 'bold'))
        self.execute_label.grid(row=2, column=95)


    def resetTextArea(self):
        self.textarea.delete(1.0, END)
        self.reset_machine()

    def reset_machine(self):
        self.memory = []
        self.PC = 0
        self.IR = -1
        self.MAR = 0
        self.accumulator = 0
        MainFrame.pipelinelist = []
        for i in range(100):
            self.memory.append(0)
        self.update_CPUState()
        self.update_memoryTable()
        self.update_output()

    def exit(self):
        exit()

    def iterate_linesRest(self):
        for line in self.textarea.get('1.0', 'end-1c').splitlines():
            # Iterate lines
            if line:
                MainFrame.pipelinelist.append(line)
        MainFrame.pipelinelist = [x for x in MainFrame.pipelinelist if "DEC" not in x]
        MainFrame.pipelinelist.extend(['', ''])
        q = deque(['', '', ''])
        for i, val in enumerate(MainFrame.pipelinelist):
            q.pop()
            q.appendleft(val)
            for j, label in enumerate(q):
                self.stageLabel = Label(self, text=str(label)).grid(column=j+93, row=i + 4)

    def load_file(self, text_box):
        # Delete previous text
        # Grab Filename
        program_file = filedialog.askopenfilename(
            title="Open File",
            filetypes=(("Program Files", "*.txt"),
                       ("All Types", "*.*")))

        # Load the program
        program_file = open(program_file, 'r')
        program = program_file.read()
        # Put program context into gui
        text_box.insert(END, program)
        # Close opened file
        program_file.close()

    def save_file(self, text_box):
        program_file = filedialog.asksaveasfilename(
            title="Save File",
            filetypes=(("Program Files", "*.txt"),))
        # If user doesn't press cancel in dialog
        if program_file:
            # Save the program
            program_file = open(program_file, 'w')
            program_file.write(text_box.get(1.0, END))
            program_file.close()

    def pipeline_reader(op_string):
        opcode, values = op_string.split(" ")
        values_list = values.split(',')
        instr = []
        hazard = []
        dest = values_list[0]
        src = values_list[1:]
        list_of_all = [hazard for item in instr]
        opcodes = [op[0] for op in list_of_all]
        dests = [dest[1] for dest in list_of_all]
        srcs = [src[2] for src in list_of_all]
        dep_list = [opcodes[i] for i, dest in enumerate(dests) for src in srcs if dest in src]

        return (dep_list)



def main():
    root = Tk()
    root.geometry("2560x1440")
    app = MainFrame(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
