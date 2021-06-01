import sys

# conflicting_opcodes in hexadecimal.
conflicting_opcodes = ["0C", "30", "32", "33", "34", "36", "37", "3C", "3E", "3F", "40", "42", "43", "49", "4A", "4B",
					   "4D", "4E", "4F", "51", "52", "53", "55", "56", "57", "59", "5A", "5B", "5D", "5E", "5F", "61", "62", "63", "65", "66", "67", "69",
					   "6A", "6B", "6C"]
branch_map = {}


infile_name = sys.argv[1]
outfile_name = sys.argv[2]

branch_map = {}
infile =  open(infile_name, 'r') #To read the file.
outfile = open(outfile_name, 'w') #To append, if we open with w, it overwrites.


def stop_everything():
	print("There is a syntax error or impossible addressing mode")
	open("myoutput1.txt", 'w').close()  # Deletes the content.
	sys.exit()  # Stops execution.


def conflicting_opcode_and_add_mode(hexa_byte):
	if hexa_byte in conflicting_opcodes:
		return True
	else:
		return False


def is_valid_branch_name(str):
	if len(str) > 1 and str.endswith(':'):
		return True
	else:
		return False


# 18 --> 0012 or 8--> 08, second parameter defines the length.
def num_to_n_digit_hex(num, n=0):
	num = hex(num)[2:]  # Convert to hex and remove "1x" from the beginning.
	length = len(num)

	beginning = ""
	for i in range(n - length):
		beginning += "0"

	result = beginning + str(num)
	return result.upper()


# Takes a character of the form 'A', 'B', 'R' etc. and returns the corresponding ASCII character in hexadecimal.
def character_to_four_digit_hex(ch):
	decimal = ord(ch)

	return num_to_n_digit_hex(decimal, 4)


# Either 123 or 'A', 'B' or branch name.
def immediate_to_binary(str):
	if ishexanum(str):
		return str
	elif len(str) == 3 and str[0] == '\'' and str[len(str) - 1] == '\'':
		return character_to_four_digit_hex(str[1])
	elif str in branch_map.keys():
		return branch_map.get(str)

	return "fucked up"


# Takes register name and returns the corresponding binary number for that register.
def register_to_binary(str):
	if str == 'PC':
		return "0000"
	elif str == 'A':
		return "0001"
	elif str == 'B':
		return "0002"
	elif str == 'C':
		return "0003"
	elif str == 'D':
		return "0004"
	elif str == 'E':
		return "0005"
	elif str == 'S':
		return "0006"


# Returns true if string is a number.
def ishexanum(str):
	for i in str:
		if i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9' or i == 'A' or i == 'B' or i == 'C' or i == 'D' or i == 'E' or i == 'F':
			continue
		else:
			return False

	return True


# Either direct number such as 145. Or a character in the form of 'A', 'c' '*' etc. Or name of a branch.
def isImmediate(str):
	# Direct number.
	if ishexanum(str):
		return True

	# An ASCII character.
	if len(str) == 3 and str[0] == '\'' and str[2] == '\'':
		return True

	# Memory adress of the branch. We take it as immediate.
	if str in branch_map.keys():
		return True

	return False


# Returns true if string is a register name
def isRegister(str):
	if str == 'PC' or str == 'A' or str == 'B' or str == 'C' or str == 'D' or str == 'E' or str == 'S':
		return True

	return False


# Returns true if string is a register memory Duzeltilmesi lazim !!!!!!!!!!!!!!!!!!!!!!!!!!!
def isRegisterMemory(str):
	if str[0] == '[' and str[len(str) - 1] == ']' and isRegister(str[1:len(str) - 1]):
		return True

	return False


# Returns true if string is a memory
def isMemory(str):
	if str[0] == '[' and str[len(str) - 1] == ']' and ishexanum(str[1:len(str) - 1]):
		return True

	return False


# LOAD sth
# SUB sth
# JE sth			I am taking this sth and handle it. I assume one 1 whitespace exist between the two!!!!!!!!
def get_addressing_mode(str):
	if (isRegister(str)):
		return "01"
	elif (isImmediate(str)):
		return "00"
	elif (isRegisterMemory(str)):
		return "10"
	elif (isMemory(str)):
		return "11"

	stop_everything()


def handle(token2, opcode):
	add_mode = get_addressing_mode(token2)  # it is sth like "00", "01", "10", "11".
	binary_byte = opcode + add_mode  # Something like "00101100"
	decimal_byte = int(binary_byte, 2)  # Second argumant is base. it returns number. Not string!!
	hexa_byte = num_to_n_digit_hex(decimal_byte, 2)
	# print(hexa_byte)

	outfile.write(hexa_byte)  # First 2 characters of the binary instruction.

	if conflicting_opcode_and_add_mode(str(hexa_byte)):
		print("conflicting_opcode_add_mode")
		stop_everything()

	if (add_mode == "00"):
		outfile.write(immediate_to_binary(token2))
	elif (add_mode == "01"):
		outfile.write(register_to_binary(token2))
	elif (add_mode == "10"):
		outfile.write(register_to_binary(token2[1: len(token2) - 1]))
	elif (add_mode == "11"):
		outfile.write(token2[1: len(token2) - 1])  # This is already given as a hexadecimal.

	outfile.write("\n")


def handle_execution(execution_tokens):
	if len(execution_tokens) == 0:  #This cannot catch empty lines, instead it goes into length 1 case.
		return

	if len(execution_tokens) > 2:  # There cannot be more than 2 tokens.
		stop_everything()

	token1 = execution_tokens[0]

	if len(execution_tokens) == 1:
		if token1[
		   : len(token1) - 1] in branch_map.keys():  # branch name. To get around the ":" at the end of label name.
			return
		elif token1 == "HALT":
			outfile.write("040000\n")
		elif token1 == "NOP":
			outfile.write("380000\n")
		elif token1 == "":  #Empty string !!!!!!
			return
		else:
			stop_everything()  # Syntax error.

	if len(execution_tokens) == 2:

		if token1 == "LOAD":
			handle(execution_tokens[1], "000010")
		elif token1 == "STORE":
			handle(execution_tokens[1], "000011")
		elif token1 == "ADD":
			handle(execution_tokens[1], "000100")
		elif token1 == "SUB":
			handle(execution_tokens[1], "000101")
		elif token1 == "INC":
			handle(execution_tokens[1], "000110")
		elif token1 == "DEC":
			handle(execution_tokens[1], "000111")
		elif token1 == "XOR":
			handle(execution_tokens[1], "001000")
		elif token1 == "AND":
			handle(execution_tokens[1], "001001")
		elif token1 == "OR":
			handle(execution_tokens[1], "001010")
		elif token1 == "NOT":
			handle(execution_tokens[1], "001011")
		elif token1 == "SHL":
			handle(execution_tokens[1], "001100")
		elif token1 == "SHR":
			handle(execution_tokens[1], "001101")
		elif token1 == "PUSH":
			handle(execution_tokens[1], "001111")
		elif token1 == "POP":
			handle(execution_tokens[1], "010000")
		elif token1 == "CMP":
			handle(execution_tokens[1], "010001")
		elif token1 == "JMP":
			handle(execution_tokens[1], "010010")
		elif token1 == "JZ" or token1 == "JE":
			handle(execution_tokens[1], "010011")
		elif token1 == "JNZ" or token1 == "JNE":
			handle(execution_tokens[1], "010100")
		elif token1 == "JC":
			handle(execution_tokens[1], "010101")
		elif token1 == "JNC":
			handle(execution_tokens[1], "010110")
		elif token1 == "JA":
			handle(execution_tokens[1], "010111")
		elif token1 == "JAE":
			handle(execution_tokens[1], "011000")
		elif token1 == "JB":
			handle(execution_tokens[1], "011001")
		elif token1 == "JBE":
			handle(execution_tokens[1], "011010")
		elif token1 == "READ":
			handle(execution_tokens[1], "011011")
		elif token1 == "PRINT":
			handle(execution_tokens[1], "011100")
		else:
			stop_everything()


def main():
	line_list = infile.readlines()  # Elements also have \n at the end!!! I may need to delete them.

	for i in range(len(line_list)):
		line_list[i] = line_list[i].strip()  # Remove white spaces from the beginning and end.
		line_list[i] = line_list[i].split(" ")  # Now line_list[i] contains both first and second operand.

	# This one keeps the (branch name : memory adress) pairs. Memory adress is in hex digits.
	# This iteration is for setting branch_map variable and removing white spaces from beginning and end

	memory_counter = 0
	for curr_line in line_list:
		if ':' in curr_line[0]:
			branch_map[curr_line[0].replace(":", "")] = num_to_n_digit_hex(memory_counter, 4)
			continue  # Don't increase memory_counter, branch is not an instruction!
		if curr_line[0] == "":
			continue

		memory_counter += 3

	# print(branch_map)
	for execution_tokens in line_list:
		# print(execution_tokens)
		handle_execution(execution_tokens)

	infile.close()
	outfile.close()


main()  # Calling main.