from tkinter import *
from tkinter import filedialog
import os


def load_file(text_box):
    local = os.getcwd()
    #Delete previous text
    text_box.delete("1.0", END)
    
    #Grab Filename
    program_file = filedialog.askopenfilename(initialdir=f"{local}/saved_programs", 
                                            title = "Open File", 
                                            filetypes =(("Program Files", "*.txt"), 
                                                        ("All Types", "*.*")))
    
    #Load the program
    program_file = open(program_file, 'r')
    program = program_file.read()
    #Put program context into gui
    text_box.insert(END, program)
    #Close opened file
    program_file.close()

def save_file(text_box):
    local = os.getcwd()
    program_file = filedialog.asksaveasfilename(defaultextension = ".*",
                                                initialdir=f"{local}/saved_programs",
                                                title="Save File",
                                                filetypes = (("Program Files", "*.txt"),))
    #If user doesn't press cancel in dialog
    if program_file:
        #Save the program
        program_file = open(program_file, 'w')
        program_file.write(text_box.get(1.0, END))
        program_file.close()