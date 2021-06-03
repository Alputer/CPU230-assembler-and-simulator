import sys

register = [0,0,0,0,0,0, 2**16-2]  #[PC, A, B, C, D, E, S]   S is the last memory address
flag = {'zf':False, 'cf':False, 'sf':False}  #flags


ram = dict()    #this deictionary represents the ram (memory) of the machine
				#debugging is easier with a dictionary.

instruction_list = []  #the list of instruction objects


# keys represents instructions. The items are instructions' possible addressing modes.
appropriate_address_modes = {
	1: [0,1,2,3],  #HALT may be different
	2: [0,1,2,3],
	3: [1,2,3],
	4: [0,1,2,3],
	5: [0,1,2,3],
	6: [0,1,2,3],
	7: [0,1,2,3],
	8: [0,1,2,3],
	9: [0,1,2,3],
	10: [0,1,2,3],
	11: [0,1,2,3],
	12: [1],
	13: [1],
	14: [0,1,2,3],  # ?
	15: [1],
	16: [1],
	17: [0,1,2,3],
	18: [0],
	19: [0],
	20: [0],
	21: [0],
	22: [0],
	23: [0],
	24: [0],
	25: [0],
	26: [0],
	27: [1,2,3],
	28: [0,1,2,3]
}

input_queue = [] 	# contains the consol input token by token. (tokens are seperated by ' ', '\n' or '\t')
					# input: 'a bcd		ef'     input_queue = ['a', 'bcd', 'ef']
# Returns the next element of input_queue. If input_queue is empty, then waits the user to enter an input.
def get_input():
	if len(input_queue) == 0:
		new_inp = input()
		input_queue.extend(new_inp.split())  # tokens are seperated by space characters.
	k = input_queue.pop(0)
	return ord(k)

# if number can't fit to 2 bytes (num>=2**16), then removes overflow bits and returns the resultant number.
# if number is negative, takes 2's complement of number and returns the result.
def fit_to_2bytes(number):
	if number < 0:
		return 2**16 + number
	return number % (2**16)


# This class represents an instruction. Gets an instruction's opcode, addresing_mode, operand information and
# executes that instruction using some useful methods.
class instruction:
	halt = False	# if it is true program is halted
	error = False	# if it is true, there is an error and program will be stopped.

	# constructor. opcode, addresing_mode and operand of this instruction should be given
	def __init__(self, opcode, addresing_mode, operand):
		self.opcode = opcode
		self.addresing_mode = addresing_mode
		self.operand = operand

	# helpful for debugging
	def __str__(self):
		return str([self.opcode, self.addresing_mode, self.operand])

	# gets the meaning (value) of operand according to addressing mode
	# if addresing_mode = 0, the value of operand is returned.
	# if addresing_mode = 1, the value in register is returned.
	# if addresing_mode = 2, the value in address to which value of the given ram points is returned.
	# if addresing_mode = 3, the value in the adress is returned
	def get_value(self):
		if self.addresing_mode == 0:
			return self.operand
		elif self.addresing_mode == 1:
			return register[self.operand]
		elif self.addresing_mode == 2:
			if register[self.operand] not in ram.keys():
				return 0   # at the begingging of the program ram values are all zeros
			else:
				return ram[register[self.operand]]
		elif self.addresing_mode == 3:
			if self.operand not in ram.keys():
				return 0
			else:
				return ram[self.operand]

	# loads the value to the given register
	def set_register_value(self, value, register_num):
		fitted_value = fit_to_2bytes(value)
		register[register_num] = fitted_value

	# loads the value to the given address
	def set_memory_value(self, value, address):
		fitted_value = fit_to_2bytes(value)
		ram[address] = fitted_value

	#sets the value to the corresponding ram address or register. Trundicates if there is an overflow and complements if
	#value is negative
	def set_value(self, value):
		fitted_value = fit_to_2bytes(value)

		if self.addresing_mode == 0:
			pass #addresing mode = 0 is not possible
		elif self.addresing_mode == 1:
			register[self.operand] = fitted_value
		elif self.addresing_mode == 2:
			ram[register[self.operand]] = fitted_value
		elif self.addresing_mode == 3:
			ram[self.operand] = fitted_value


	# sets the flags according to the given value.
	# this value is the result of the last instruction.
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


	# returns true if this instrucion may use this addressing_mode
	def check_operand_address_mode_consistency(self):
		return self.addresing_mode in appropriate_address_modes[self.opcode]


	# executes this instruction. Loads, stores, adds, prints, reads,... Handles every instruction.
	# This is the the ultimate method of this class. This method uses every other methods in this class.
	def execute(self):
		if not self.check_operand_address_mode_consistency():
			instruction.error = True
			return

		value = self.get_value()   # this value is very useful in many ways. So we get it here, outside of the if block.

		if self.opcode == 1: # HALT
			instruction.halt = True
		elif self.opcode == 2: # LOAD
			register[1] = value
		elif self.opcode == 3:  # STORE
			self.set_value(register[1])
		elif self.opcode == 4:  # ADD
			new_value = register[1] + value
			self.set_register_value(new_value, 1)
			self.set_flag(new_value)
		elif self.opcode == 5:  # SUB
			new_value = register[1] + (2**16 - value) #Take 2's complement, then add.
			self.set_register_value(new_value, 1)
			self.set_flag(new_value)
		elif self.opcode == 6:  # INC
			self.set_value(value + 1)
			self.set_flag(value + 1)
		elif self.opcode == 7:  # DEC
			not_one = 2**16 - 1
			self.set_value(value + not_one) # I take 2's complement of 1, then add.
			self.set_flag(value + not_one) # I take 2's complement of 1, then add.
		elif self.opcode == 8:  # XOR
			new_value = fit_to_2bytes(register[1] ^ value)
			old_val = flag['cf']
			self.set_register_value(new_value, 1)
			self.set_flag(new_value)
			flag['cf'] = old_val
		elif self.opcode == 9:  # AND
			new_value = fit_to_2bytes(register[1] & value)
			old_val = flag['cf']
			self.set_register_value(new_value, 1)
			self.set_flag(new_value)
			flag['cf'] = old_val
		elif self.opcode == 10:  # OR
			new_value = fit_to_2bytes(register[1] | value)
			old_val = flag['cf']
			self.set_register_value(new_value, 1)
			self.set_flag(new_value)
			flag['cf'] = old_val
		elif self.opcode == 11:  # NOT
			new_value = 2**16 - 1 - value
			old_val = flag['cf']
			self.set_value(new_value)
			self.set_flag(new_value)
			flag['cf'] = old_val
		elif self.opcode == 12:  # SHL
			new_value = value << 1
			old_val = flag['cf']
			self.set_value(new_value)
			self.set_flag(new_value)
			flag['cf'] = old_val
		elif self.opcode == 13:  # SHR
			new_value = value >> 1
			old_val = flag['cf']
			self.set_value(new_value)
			self.set_flag(new_value)
			flag['cf'] = old_val
		elif self.opcode == 14:  # NOP
			pass
		elif self.opcode == 15:  # PUSH
			self.set_memory_value(value, register[6])
			if register[6] == 0:
				instruction.error = True
			register[6] -= 2
		elif self.opcode == 16:  # POP
			register[6] += 2
			if register[6] == 2 ** 16:
				instruction.error = True
			if register[6] in ram.keys():
				self.set_value(ram[register[6]])
			else:
				self.set_value(0)
		elif self.opcode == 17:  # CMP
			new_value = register[1] + (2**16 - value)
			self.set_flag(new_value)
		elif self.opcode == 18:  # JMP
				register[0] = value
				return
		elif self.opcode == 19:  # JZ/JE
			if flag['zf'] == True:
				register[0] = value
				return
		elif self.opcode == 20:  # JNZ/JNE
			if flag['zf'] == False:
				register[0] = value
				return
		elif self.opcode == 21:  # JC
			if flag['cf'] == True:
				register[0] = value
				return
		elif self.opcode == 22:  # JNC
			if flag['cf'] == False:
				register[0] = value
				return
		elif self.opcode == 23:  # JA
			if flag['sf'] == False and flag['zf'] == False:
				register[0] = value
				return
		elif self.opcode == 24:  # JAE
			if flag['sf'] == False or flag['zf'] == True:
				register[0] = value
				return
		elif self.opcode == 25:  # JB
			if flag['sf'] == True and flag['zf'] == False:
				register[0] = value
				return
		elif self.opcode == 26:  # JBE
			if flag['sf'] == True or flag['zf'] == True:
				register[0] = value
				return
		elif self.opcode == 27:  # READ
			inp = get_input()
			self.set_value(inp)
		elif self.opcode == 28:  # PRINT
			outfile.write(chr(value) + '\n')


		register[0] += 3  # increas the program counter at the end




# code is hex string instruction code
# returns an instruction object which the given hex instruction code represents
def instruction_code_to_values(code):
	first_part = code[0:2]
	second_part = code[2:6]

	first_part_num = int(first_part, 16)
	opcode = first_part_num // 4
	addressing_mode = first_part_num % 4
	operand = int(second_part, 16)

	return instruction(opcode, addressing_mode, operand)


infile_name = sys.argv[1]
outfile_name = infile_name[: len(infile_name) -  3] + "txt"

infile =  open(infile_name, 'r') #To read the file.
outfile = open(outfile_name, 'w') #To write to the file

line_list = infile.readlines()  # line_list contains lines of input file.

for i in range(len(line_list)):
	line_list[i] = line_list[i].rstrip("\n")  # Remove "\n" from end of the string
	instruction_list.append(instruction_code_to_values(line_list[i]))


# ezecute instructions one by one till the program halts or there is an error.
while True:
	i = register[0]//3

	if(register[0] > 3 * (len(instruction_list) - 1)): #Checks whether we enter the area above the memory our commands reside.
		open(outfile_name, 'w').close()  # Deletes the content.
		sys.exit()  # Stops execution.

	instruction_list[i].execute()

	# program halts. End the program.
	if instruction.halt:
		break

	# there is an error. Delete the output the program writes so far. End the program.
	if instruction.error:
		open(outfile_name, 'w').close()  # Deletes the content.
		sys.exit()  # Stops execution.


# close the files
infile.close()
outfile.close()