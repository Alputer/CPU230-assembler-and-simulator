
branch_map = {}
infile =  open("input1.txt", 'r') #To read the file.
outfile = open("myoutput1.txt", 'w') #To append, if we open with w, it overwrites.


#18 --> 0012 or 8--> 08, second parameter defines the length.
def num_to_n_digit_hex(num,n = 0):
  num = hex(num)[2:] #Convert to hex and remove "1x" from the beginning.
  length = len(num)

  beginning = "";
  for i in range(n - length):
	beginning += "0"
	
  result =  beginning + str(num)
  return result.upper()

#Takes a character of the form 'A', 'B', 'R' etc. and returns the corresponding ASCII character in hexadecimal.
def character_to_four_digit_hex(ch):
   decimal = ord(ch)

   return num_to_n_digit_hex(decimal, 4)

#Either 123 or 'A', 'B' or branch name.
def immediate_to_binary(str):

   if ishexanum(str):
		return str
   elif len(str) == 3 and str[0] == '\'' and str[len(str) - 1] == '\'':
		return character_to_four_digit_hex(str[1])
   elif str in branch_map.keys():
	   return  branch_map.get(str)


   return "fucked up"  


#Takes register name and returns the corresponding binary number for that register.
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

#Returns true if string is a number.
def ishexanum(str):

  for i in str:
	 if i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5'or i == '6'or i == '7'or i == '8' or i == '9' or i == 'A' or i == 'B' or i == 'C' or i == 'D' or i == 'E' or i == 'F':
	   continue
	 else:
	   return False

  return True

#Either direct number such as 145. Or a character in the form of 'A', 'c' '*' etc. Or name of a branch.
def isImmediate(str):
	#Direct number.
	if ishexanum(str):
	   return True
	
	#An ASCII character.
	if len(str) == 3 and str[0] == '\'' and str[2] == '\'':
	   return True

	 #Memory adress of the branch. We take it as immediate.
	if str in branch_map.keys():
		return True

	return False

#Returns true if string is a register name
def isRegister(str):

   if str == 'PC' or str == 'A' or str == 'B' or str == 'C' or str == 'D' or str == 'E' or str == 'S':
	  return True

   return False

#Returns true if string is a register memory Duzeltilmesi lazim !!!!!!!!!!!!!!!!!!!!!!!!!!!
def isRegisterMemory(str):

  if str[0] == '[' and str[len(str) - 1] == ']' and isRegister(str[1:len(str) - 1]):
	 return True

  return False

#Returns true if string is a memory
def isMemory(str):

  if str[0] == '[' and str[len(str) - 1] == ']' and ishexanum(str[1:len(str) - 1]):
	 return True

  return False

# LOAD sth
# SUB sth
#JE sth            I am taking this sth and handle it. I assume one 1 whitespace exist between the two!!!!!!!!
def get_addressing_mode(str): 

	 if(isRegister(str)):
		return "01" 
	 elif(isImmediate(str)):
		print(str)
		return "00"
	 elif(isRegisterMemory(str)):
		return "10"   
	 elif(isMemory(str)):
		return "11"

	 return "fucked up"

def handle(execution, opcode, instr_length):
		 add_mode = get_addressing_mode(execution[instr_length + 1:]) #it is sth like "00", "01", "10", "11".
		 binary_byte = opcode + add_mode # Something like "00101100"
		 decimal_byte = int(binary_byte,2) #Second argumant is base. it returns number. Not string!!
		 hexa_byte = num_to_n_digit_hex(decimal_byte,2)
		 #print(hexa_byte)

		 outfile.write(hexa_byte)
		 if(add_mode == "00"):
			outfile.write(immediate_to_binary(execution[instr_length + 1 : ]))
		 elif(add_mode == "01"):
		   outfile.write(register_to_binary(execution[instr_length + 1:]))
		 elif(add_mode == "10"):
		   outfile.write(register_to_binary(execution[instr_length + 2: len(execution) - 1]))
		 elif(add_mode == "11"):
			outfile.write(execution[instr_length + 2 : len(execution) - 1]) #This is already given as a hexadecimal.

		 outfile.write("\n")



def handle_execution(execution):
	if execution.startswith("HALT"):
		 outfile.write("040000\n")

	elif execution.startswith("LOAD "):
		 handle(execution, "000010",4)
		 # opcode = "000010"
		 # add_mode = get_addressing_mode(execution[5:]) #it is sth like "00", "01", "10", "11".
		 # binary_byte = opcode + add_mode # Something like "00101100"
		 # decimal_byte = int(binary_byte,2) #Second argumant is base. it returns number. Not string!!
		 # hexa_byte = num_to_n_digit_hex(decimal_byte,2)
		 # print(hexa_byte)
		 # outfile.write(hexa_byte + "\n")

	elif execution.startswith("STORE "):
		 handle(execution, "000011", 5)
		 # opcode = "000011"
		 # add_mode = get_addressing_mode(execution[6:])
		 # binary_byte = opcode + add_mode
		 # decimal_byte = int(binary_byte,2)
		 # hexa_byte = num_to_n_digit_hex(decimal_byte,2)
	elif execution.startswith("ADD "):
		 handle(execution, "000100", 3)
	elif execution.startswith("SUB "):
		 handle(execution, "000101", 3)
	elif execution.startswith("INC "):
		 handle(execution, "000110", 3)
	elif execution.startswith("DEC "):
		 handle(execution, "000111", 3)
	elif execution.startswith("XOR "):
		 handle(execution, "001000", 3)
	elif execution.startswith("AND "):
		 handle(execution, "001001", 3)
	elif execution.startswith("OR "):
		 handle(execution, "001010", 2)
	elif execution.startswith("NOT "):
		 handle(execution, "001011", 3)
	elif execution.startswith("SHL "):
		 handle(execution, "001100", 3)
	elif execution.startswith("SHR "):
		 handle(execution, "001101", 3)
	elif execution.startswith("NOP "):
		 handle(execution, "00111", 3)
	elif execution.startswith("PUSH "):
		 handle(execution, "001111", 4)
	elif execution.startswith("POP "):	
		 handle(execution, "010000", 3)
	elif execution.startswith("CMP "):
		 handle(execution, "010001", 3)
	elif execution.startswith("JMP "):
		 handle(execution, "010010", 3)
	elif execution.startswith("JZ ") or execution.startswith("JE "):
		 handle(execution, "010011", 2)
	elif execution.startswith("JNZ ") or execution.startswith("JNE "):
		 handle(execution, "010100", 3)
	elif execution.startswith("JC "):
		 handle(execution, "010101", 2)
	elif execution.startswith("JNC "):
		 handle(execution, "010110", 3)
	elif execution.startswith("JA "):
		 handle(execution, "010111", 2)
	elif execution.startswith("JAE "):
		 handle(execution, "011000", 3)
	elif execution.startswith("JB "):
		 handle(execution, "011001", 2)
	elif execution.startswith("JBE "):
		 handle(execution, "011010", 3)
	elif execution.startswith("READ "):
		 handle(execution, "011011", 4)
	elif execution.startswith("PRINT "):
		 handle(execution, "011100", 5)


def main():

  #PC = 0; # Program counter. After executing each line, it is increased by 3.

  line_list = infile.readlines() #Elements also have \n at the end!!! I may need to delete them.

  for i in range(len(line_list)):
	 line_list[i] = line_list[i].strip() #Remove white spaces from the beginning and end.
	 line_list[i] = line_list[i].rstrip("\n") #Remove "\n" from end of the string



   # This one keeps the (branch name : memory adress) pairs. Memory adress is in hex digits.
#This iteration is for setting branch_map variable and removing white spaces from beginning and end

  memory_counter = 0
  for curr_line in line_list:
	  if ':' in curr_line:
		  branch_map.update({curr_line.replace(":", "") : num_to_n_digit_hex(memory_counter, 4)}) # Add function.
		  continue #Don't increase memory_counter, branch is not an instruction !!!!!
	  memory_counter += 3

  print(branch_map)
  for execution in line_list:
	  handle_execution(execution)
  


  infile.close()
  outfile.close()

main() #Calling main.

