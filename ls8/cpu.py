"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 
        self.pc = 0 
        self.reg = [0] * 8
        self.running = True
        self.machine = {
            'MUL':0b10100010,
            'HLT':0b00000001,
            'LDI':0b10000010,
            'PRN':0b01000111,
            'PUSH':0b01000101,
            'POP':0b01000110
            }
        

    def load(self):
        """Load a program into memory."""
        address = 0
        file_name = sys.argv[1]
        if len(sys.argv) < 2:
            print("Need to input a second file name: python3 first_file_name.py second_file_name.py")
            sys.exit(1)
        try:
            with open(file_name) as file:
                for line in file:
                    print("line: ", line)
                    split_line = line.split("#")
                    command = split_line[0].strip()
                    print("command: ", command)
                    if command == "":
                        continue
                    instruction = int(command, 2)
                    print(f"{instruction:8b} is {instruction}")
                    
                    self.ram[address] = instruction
                    
                    address += 1
                    print("Ram: ", self.ram)
        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[0]}:{sys.argv[1]}")
            sys.exit(2)

            if address == 0:
                print("Program was empty")
                sys.exit(3)

        # For now, we've just hardcoded a program:
        # program = [
        #   # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, counter):
        return self.ram[counter]
    def ram_write(self, counter, MDR): #MDR value
        self.reg[counter] = MDR
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # value = op >> 6
        # value = value + 1
        #print("value: ", value)
       
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            print("MUL results: ",self.reg[reg_a] * self.reg[reg_b])
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
            #sys.exit()

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        #  0b10000010 
        pc = self.pc
        self.reg[7] = 0xF4
        
        #Add the HLT instruction definition
        # HLT = 0b00000001 
        # LDI = 0b10000010
        # PRN = 0b01000111
        # MUL = 0b10100010

        while self.running:
            #self.alu(ir[self.ram_read(pc)], self.ram_read(pc+1), self.ram_read(pc+2))
            #Instruction Register. Read memory address stored in pc
            ir = self.ram_read(pc)
           
            if ir == self.machine["HLT"]:
                #exit the program
                self.running = False
                pc += 1
                sys.exit()
            if ir == self.machine["LDI"]:
                #This instruction sets a specified register to a specified value,
               
                self.ram_write(self.ram_read(pc+1), self.ram_read(pc+2))
                print("LDI, pc, pc+1: ", ir, self.ram_read(pc+1), self.ram_read(pc+2))
                #self.trace()
                pc += 3
            if ir == self.machine["PRN"]:
                #Print to the console the decimal integer value that is stored in the given register
                reg_num = self.ram[pc + 1]
                print(self.reg[reg_num])  
                pc += 2
            if ir == self.machine["MUL"]:
                reg_a = self.ram_read(pc + 1)
                reg_b = self.ram_read(pc +2)
                self.alu("MUL", reg_a, reg_b)
                pc += 3
            if ir == self.machine["PUSH"]:
                #stack pointer decrement
                self.reg[7] -= 1
                #get value from the register number
                reg = self.ram[pc+1]
                #get the value from the given register
                value = self.reg[reg]
                #put it on the stack at the pointer address
                sp = self.reg[7]
                self.ram[sp] = value
                self.trace()
                pc += 2

            if ir == self.machine["POP"]:
                # get the stack pointer (where do we look?)
                sp = self.reg[7]
                # get register number to put value in
                reg = self.ram[pc+1]
                # use stack pointer to get the value
                value = self.ram[sp]
                #put the value into the given register
                self.reg[reg] = value
                #increment our stack pointer
                self.reg[7] += 1
                # icnrement our program counter
                #self.trace()
                pc += 2