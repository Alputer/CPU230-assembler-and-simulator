register = [0,0,0,0,0,0,0]  #[PC, A, B, ...]
flag = {'zf':False, 'cf':False, 'sf':False}



#ram = [0 for i in range(2**16)] #ram[0] has the integer of first 8bits, ram[8] has the integer of the second 8bits,...
                                #so index 1,2,3,4,5,6,7 aren't used.
                                #only byte access is available for this projects so I can do this.

ram = dict()    #checking the truthness of this is easier so I used this one.
                #but upper one is faster. If speed is needed upper one should be used.

instruction_list = []

halt = False


def fit_to_2bytes(number):
    if number < 0:
        return 2**16 + number
    return number % (2**16)


class instruction:
    #opcode     addresing_mode      operand
    def __init__(self, opcode, addresing_mode, operand):
        self.opcode = opcode
        self.addresing_mode = addresing_mode
        self.operand = operand

    def __str__(self):
        return str([self.opcode, self.addresing_mode, self.operand])

    #gets the meaning (value) of operand according to addressing mode
    def get_value(self):
        if self.addresing_mode == 0:
            return self.operand
        elif self.addresing_mode == 1:
            return register[self.operand]
        elif self.addresing_mode == 2:
            if register[self.operand] not in ram.keys():
                return 0
            else:
                return ram[register[self.operand]]
        elif self.addresing_mode == 3:
            if self.operand not in ram.keys():
                return 0
            else:
                return ram[self.operand]
        else:
            print("ERROR: instruction.get_value() ")

    #loads the value to the given register
    def set_register_value(self, value, register_num):
        fitted_value = fit_to_2bytes(value)
        register[register_num] = fitted_value

    #sets value to the corressponding ram address or register. Trundicates if there is an overflow and complements if
    #value is negative
    def set_value(self, value):
        fitted_value = fit_to_2bytes(value)

        if self.addresing_mode == 0:
            print("ERROR: set_value")
        elif self.addresing_mode == 1:
            register[self.operand] = fitted_value
        elif self.addresing_mode == 2:
            ram[register[self.operand]] = fitted_value
        elif self.addresing_mode == 3:
            ram[self.operand] = fitted_value
        else:
            print("ERROR: instruction.set_value() ")


    #I am not sure how flags work. So double check here
    def set_flag(self, value):
        if value >= 2**16:
            flag['cf'] = True
        else:
            flag['cf'] = False

        value = fit_to_2bytes(value)

        if value == 0:
            flag['zf'] = True
        else:
            flag['zf'] = False

        if value >= 2**15:
            flag['sf'] = True
        else:
            flag['sf'] = False



    def execute(self):
        value = self.get_value()

        if self.opcode == 1: #halt
            print("halting...")
            halt = True
        elif self.opcode == 2: #load
            register[1] = value
        elif self.opcode == 3:  # store
            self.set_value(register[1])
        elif self.opcode == 4:  # add
            new_value = register[1] + value
            self.set_register_value(new_value, 1)
            self.set_flag(new_value)
        elif self.opcode == 5:  # SUB
            new_value = register[1] - value
            self.set_register_value(new_value, 1)
            self.set_flag(new_value)
        elif self.opcode == 6:  # inc
            self.set_value(value+1)
            self.set_flag(value+1)
        elif self.opcode == 7:  # dec
            self.set_value(value-1)
            self.set_flag(value-1)
        elif self.opcode == 20:  # JNZ/JNE
            if flag['zf'] == False:
                register[0] = value
                return
        elif self.opcode == 28:  # print
            outfile.write(chr(value) + '\n')
            print("PRINT:", chr(value))


        register[0] += 3  # increas program counter at the end




#code is hex string instruction code
#returns an instruction object
def instruction_code_to_values(code):
    first_part = code[0:2]
    second_part = code[2:6]

    first_part_num = int(first_part, 16)
    opcode = first_part_num // 4
    addressing_mode = first_part_num % 4
    operand = int(second_part, 16)

    return instruction(opcode, addressing_mode, operand)




infile =  open("input2.txt", 'r') #To read the file.
outfile = open("myoutput2.txt", 'w') #To append, if we open with w, it overwrites.

line_list = infile.readlines()  # Elements also have \n at the end!!! I may need to delete them.

for i in range(len(line_list)):
    #line_list[i] = line_list[i].strip()  # Remove white spaces from the beginning and end.
    line_list[i] = line_list[i].rstrip("\n")  # Remove "\n" from end of the string
    instruction_list.append(instruction_code_to_values(line_list[i]))

print(register)
print()


while True:
    i = register[0]//3
    print(str(i)+':', str(instruction_list[i]), "(" + line_list[i] + ")")
    instruction_list[i].execute()

    print(register)
    print(ram)
    print()

    if halt:
        break


print(ram)

infile.close()
outfile.close()