infile =  open("input2.txt", 'r') #To read the file.
outfile = open("myoutput2.txt", 'w') #To append, if we open with w, it overwrites.

PC = 0
A = 0
B = 0
C = 0
D = 0
E = 0
S = 0
CF = 0
SF = 0 #1 if negative, 0 if positive.
ZF = 0
stack = [] #I use list as a stack. Use only append() and pop() methods !!!
memory_vals = {} #This one keeps [memory1 - value1] , [memory2 - value2] , ..... etc.



#Binary to decimal.
def my_conversion(str):

  result = 0
  for i in range(len(str)):
       result += (2**i) * int(str[len(str) - 1 - i])

  return result

def get_opcode(str): #Don't need to check halt, it is handled in the main function.

	if str == "000010":
	   return "LOAD"
	elif str == "000011":
	   return "STORE"
	elif str == "000100":
	   return "ADD"
	elif str == "000101":
	   return "SUB"
	elif str == "000110":
	   return "INC"
	elif str == "000111":
	   return "DEC"
  elif str == "001000":
	   return "XOR"
	elif str == "001001":
	   return "AND"
	elif str == "001010":
	   return "OR"
	elif str == "001011":
	   return "NOT"
	elif str == "001100":
	   return "SHL"
	elif str == "001101":
	   return "SHR"
	elif str == "001110":
	   return "NOP"
	elif str == "001111":
	   return "PUSH"
	elif str == "010000":
	   return "POP"
	elif str == "010001":
	   return "CMP"
	elif str == "010010":
	   return "JMP"
	elif str == "010011":
	   return "JZ" #Same as "JE"
	elif str == "010100":
	   return "JNZ" #Same as "JZE"
  elif str == "010101":
	   return "JC"
	elif str == "010110":
	   return "JNC"
	elif str == "010111":
	   return "JA"
  elif str == "011000":
	   return "JAE"
	elif str == "011001":
	   return "JB"
	elif str == "011010":
	   return "JBE"
  elif str == "011011":
	   return "READ"
	elif str == "011100":
	   return "PRINT"
	      
  return "fucked up"


def get_add_mode(str):
	if str == "00":
	  return "IMMEDIATE"
	elif str == "01":
	  return "REGISTER"
  elif str == "10":
    return "REGISTER_MEMORY"
  elif str == "11":
    return "MEMORY"

  return "fucked up"

def get_register_value(operand):
	  if(operand = 0):
	     return PC
	  elif(operand == 1):
	     return A
	  elif(operand == 2):
	     return B
	  elif(operand == 3):
	     return C
	  elif(operand == 4):
	     return D
	  elif(operand == 5):
	     return E
	  elif(operand == 6):
	     return S

	  return "fucked up"


#This function is used for getting the value of the operand. If we need to change & set the value of a register or a memory location, than we
# Should write another function for that.
def get_operand_value(add_mode, operand):


   operand_value_in_decimal = my_conversion(operand) #011010 --> 26

   if(add_mode == "IMMEDIATE"):
        return operand_value_in_decimal
   elif(add_mode == "REGISTER"):
        return get_register_value(operand)
   elif(add_mode == "REGISTER_MEMORY"):
   	    register_val = get_register_value(operand)
   	    return memory_vals[register_val]
   elif(add_mode == "MEMORY"):
   	    return memory_vals[operand_value_in_decimal]


   return "fucked up"
  
def execute_instruction(opcode, add_mode, operand):

  
  operand_value = get_operand_value(add_mode, operand) #operand value is in decimal form.

  if(opcode == "LOAD"):
	  pass
	elif(opcode == "STORE"):
		pass
	elif(opcode == "ADD"):
		pass
	elif(opcode == "SUB"):
		pass
	elif(opcode == "INC"):
		pass
	elif(opcode == "DEC"):
		pass
	elif(opcode == "XOR"):
		pass
	elif(opcode == "AND"):
		pass
	elif(opcode == "OR"):
		pass
	elif(opcode == "NOT"):
		pass
	elif(opcode == "SHL"):
		pass
	elif(opcode == "SHR"):
		pass
	elif(opcode == "NOP"): #Do nothing.
	  PC += 1
		return
  elif(opcode == "PUSH"):
		pass
	elif(opcode == "POP"):
		pass
	elif(opcode == "CMP"):
		pass

	elif(opcode == "JMP"):

		PC = operand_value / 3

	elif(opcode == "JZ"): #I don't need to check for "JE" since I assign them as "JZ"
		   if(ZF == 1)
		     PC = operand_value / 3
		   else
		     PC += 1

	elif(opcode == "JNZ"):
       if(ZF == 0)
         PC = operand_value / 3
       else
         PC += 1

	elif(opcode == "JC"):
		    if(CF == 1)
		      PC = operand_value / 3
		    else
		      PC += 1

	elif(opcode == "JNC"):
		    if(CF == 0)
		      PC = operand_value / 3
		    else 
		      PC += 1

	elif(opcode == "JA"):
		   	if(SF == 0 and ZF == 0)
		      PC = operand_value / 3
		    else 
		      PC += 1

	elif(opcode == "JAE"):
				if(SF == 0 or ZF == 1)
		      PC = operand_value / 3
		    else PC += 1

	elif(opcode == "JB"):
		    if(SF == 1 and ZF == 0)
		      PC = operand_value / 3
		    else 
		      PC += 1

	elif(opcode == "JBE"):
	      if(SF == 1 or ZF == 1)
		      PC = operand_value / 3
		    else 
		      PC += 1

	elif(opcode == "READ"):
		pass
	elif(opcode == "PRINT"):
		pass

	


def main():

	global PC #I didn't understand why I need this one, I used without this in the previous part?

	instr_list = infile.readlines()

	for i in range(len(instr_list)):
	 instr_list[i] = instr_list[i].strip() #Remove white spaces from the beginning and end.
	 instr_list[i] = instr_list[i].rstrip("\n") #Remove "\n" from end of the string


	while PC < len(instr_list): #Check also if we reach any halt statement.
		 
     if(instr_list[PC] == "040000"):  #Halt command. Finish the process.
        break

		 curr_instr_in_hex = "0x" + str(instr_list[PC])
		 curr_instr_in_binary = bin(curr_instr_in_hex)[2:]
     opcode = get_opcode(curr_instr_in_binary[0:6]) # I produce the string from binary code for readibility purposes.
     add_mode = get_add_mode(curr_instr_in_binary[6:8]) # I produce the string from binary code for readibility purposes.
     operand = curr_instr_in_binary[8:]
     
     execute_instruction(opcode, add_mode_ operand)




	infile.close()
	outfile.close()

main()