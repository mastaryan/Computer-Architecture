"""CPU functionality."""
import sys

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.running = True

        # Storage
        self.ram = [0] * 256
        self.registers = [0] * 8

        # Pointers
        self.pc = 0
        self.sp = 7

        # Flags
        self.fl = 0b00000000

        # Reference Table
        self.branchtable = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100000: self.ADD,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE
        }
    
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
    
    def HLT(self, a, b):
        self.running = False

    def LDI(self, a, b):
        self.registers[a] = b
        self.pc += 3

    def PRN(self, a, b):
        print(self.registers[a])
        self.pc += 2
    
    def ADD(self, a, b):
        self.alu("ADD", a, b)
        self.pc += 3

    def MUL(self, a, b):
        self.alu("MUL", a, b)
        self.pc += 3
    
    def PUSH(self, a, b):
        self.sp -= 1
        self.ram[self.sp] = self.registers[a]
        self.pc += 2

    def POP(self, a, b):
        self.registers[a] = self.ram[self.sp]
        self.ram[self.sp] = 0
        self.sp += 1
        self.pc += 2
    
    def CALL(self, a, b):
        return_address = self.pc + 2
        self.registers[self.sp] -= 1
        self.ram[self.registers[self.sp]] = return_address
        self.pc = self.registers[a]

    def RET(self, a, b):
        return_address = self.ram[self.registers[self.sp]]
        self.registers[self.sp] += 1
        self.pc = return_address

    def CMP(self, a, b):
        self.fl = 0b00000000
        self.alu('CMP', a, b)
        self.pc += 3

    def JMP(self, a, b):
        address = self.registers[a]
        self.pc = address

    def JEQ(self, a, b):
        address = self.registers[a]
        
        if self.fl == 0b00000001:
            self.pc = address
        else:
            self.pc += 2

    def JNE(self, a, b):
        address = self.registers[a]

        if self.fl != 0b00000001:
            self.pc = address
        else:
            self.pc += 2

    def load(self, file):
        """Load a program into memory."""
        address = 0

        with open(file) as f:
            for line in f:
                if line[0] == '\n' or line[0] == '#':
                    continue

                binary_code = line[:8]
                ram_value = int(binary_code, 2)

                self.ram[address] = ram_value
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        elif op == "CMP":
            if self.registers[reg_a] < self.registers[reg_b]:
                self.fl = 0b00000100
            elif self.registers[reg_a] > self.registers[reg_b]:
                self.fl = 0b00000010
            elif self.registers[reg_a] == self.registers[reg_b]:
                self.fl = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

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
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.branchtable[IR](operand_a, operand_b)