"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
RET = 0b00010001
CALL = 0b01010000
ADD = 0b10100000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # program counter
        self.pc = 0  # program counter
        # 8 new registers
        self.reg = [0] * 8  # register
        # memory storage for ram
        self.ram = [0] * 256
        self.sp = 0xF3  # stack pointer - points at the value at the top of the stack

        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt()
        self.branchtable[LDI] = self.handle_ldi()
        self.branchtable[PRN] = self.handle_prn()
        self.branchtable[MUL] = self.handle_mul()
        self.branchtable[POP] = self.handle_pop()
        self.branchtable[PUSH] = self.handle_push()
        self.branchtable[RET] = self.handle_ret()
        self.branchtable[CALL] = self.handle_call()
        self.branchtable[ADD] = self.handle_add()

    def load(self):
        """Load a program into memory."""

        address = 0
        print("loading instructions")
        # open file from cmd line
        with open(sys.argv[1]) as instructions:
            # iterate over lines in file
            for instruction in instructions:
                # grabs binary instruction from line
                instr = instruction.split("#")[0].strip()
                if instr == "":
                    continue
                # cast to binary integer
                i = int(instr, 2)
                # stores the int in ram
                self.ram[address] = i
                # increment address location
                address += 1

    def alu(self, op, operand_a, operand_b):
        """ALU operations."""
        # these are for math ops
        if op == "ADD":
            self.reg[operand_a] += self.reg[operand_b]
        elif op == "MUL":
            self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU.
        read the memory address that's stored in register `PC`, and store
        that result in `IR`, the _instruction_register Register_
        
        read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` 
        and `operand_b` in case the instruction_register needs them.
        
        the `PC` needs to be updated to point to the next instruction_register 
        for the next iteration of the loop in `run()`"""

        # _instruction_register Register_ contains a copy of the currently executing instruction_register

        # read the memory address that's stored in register `PC`, and store that result in `IR`
        while True:
            print("op")
            instruction_register = self.ram_read(self.pc)
            print(instruction_register)
            if instruction_register in self.branchtable.keys():
                self.branchtable[instruction_register]()
            else:
                print(f"instruction_register{hex(instruction_register)} not recognized")
                break

    def handle_hlt(self):
        sys.exit()

    def handle_ldi(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        print("LDI pc + 3")
        self.pc = self.pc + 3

    def handle_prn(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        print("PRN pc + 2")
        self.pc = self.pc + 2

    def handle_mul(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)
        self.pc = self.pc + 3

    def handle_add(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3

    def handle_pop(self):
        """
        Pop the value at the top of the stack into the given register.

        Copy the value from the address pointed to by SP to the given register.
        Increment SP.
        """
        operand_a = self.ram_read(self.pc + 1)
        self.reg[operand_a] = self.ram_read(self.sp + 1)
        self.sp += 1
        self.pc += 2

    def handle_push(self, operand_a, operand_b):
        """
        Decrement the SP.
        Copy the value in the given register to the address pointed to by SP
        """
        operand_a = self.ram_read(self.pc + 1)
        self.ram_write(self.sp, self.reg[operand_a])
        self.pc += 2
        self.sp -= 1

    def handle_call(self):
        operand_a = self.ram_read(self.pc + 1)
        self.sp -= 1
        self.ram_write(self.sp, self.pc + 2)
        self.pc = self.reg[operand_a]

    def handle_ret(self):
        self.pc = self.ram_read(self.sp)
        self.sp += 1

    def ram_read(self, address_to_read):
        """accept the address to read and return the value stored there."""
        return self.ram[address_to_read]

    def ram_write(self, address_to_read, register_to_write_to):
        """accept a value to write, and the address to write it to."""
        self.ram[address_to_read] = register_to_write_to
