from minic_symtab import SymTab

class State:
    def __init__(self):
        self.initialize()

    def initialize(self):
        # symbol table to hold variable-value associations
        self.symbol_table = SymTab()
        # when done parsing this variable will hold our AST
        self.AST = None
        
        #Holds floats that are used in program so ouput
        #knows what floats to allocate in the constant pool table
        #of the .class file
        self.floats = [] 

        self.strings = []

state = State()
