#command shift back
from pathlib import Path 

project = Path(__file__).resolve().parent # ****Added resolve() to get the absolute path of the current file and then get its parent directory. This will allow it to work on any computer without needing to change the path.

file_path = project / 'raw_text.txt' 
file_path1 = project / 'encrypted_text.txt'
file_path2 = project / 'decryption.txt'

for attempt in range (5):
    try: 
          shift_num1 = int (input (f'You have 5 attempts, this is {attempt + 1}/5 enter a valid number :'))
          break
    
    except ValueError:
          print ('That is not a valid number, please try again !')

else: 
    print ('You failed to enter a valid number 5 times for your first number, please try again later')
    exit()

for attempt in range (5):
    try: 
          shift_num2 = int (input (f'You have 5 attempts, this is {attempt + 1}/5 enter a valid number :'))
          break
    
    except ValueError:
          print ('That is not a valid number, please try again !')

else: 
     print('You failed to enter a valid number 5 times for your second number, please try again later')
     exit()

# Progam seemed to loop past 5 incorrect attempts - Removed the function and used print - added an exit to stop the program.      
  



def shift_function (char, shift1, shift2, dig_shift1 = shift_num1, dig_shift2 = shift_num2): #this is the shift_function block which does all the sorting and character shifting
    #Lowercase a-n shift
    if 'a' <= char <= 'n':         #each one is the same structure with a different shifting movement assigned for each range of letters capitals or numbers ect

        pos = ord(char) - ord ('a')  #starts the ord of char at 'a'

        multiplier = shift1 * shift2  #multiplies the 2 shift functions

        new_pos = (pos + multiplier) % 14 #prevents the text from going over 14 letters and wraps it back around to its numerical start point within letters between a-n also adds our position to our multiplier under the new_pos

        return chr (new_pos + ord('a')) 
    #Lowercase o-z shift
    if 'o' <= char <= 'z':

        pos2 =ord(char) - ord ('o')

        addition = shift1 + shift2

        new_pos2 = (pos2 - addition) %12  #assignment reads must shift backwards - changed the + to a -.

        return chr(new_pos2 + ord('o'))
    #capital A'M shift
    if 'A' <= char <= 'M':
    
            pos3 = ord (char) - ord ('A')
    
            new_pos3 = (pos3 - shift1) %13 # *** A to M is 13 characters. %14 to 13
    
            return chr (new_pos3 + ord ('A'))
    #capital N-Z shift
    if 'N' <= char <= 'Z':
        
                pos4 = ord (char) - ord ('N')

                squared = shift2 * shift2
                
                new_pos4 = (pos4 + squared) %13 # *** N to Z is 13 characters. %14 to 13
        
                return chr (new_pos4 + ord ('N'))
    #Number shift 0-9
    if '0' <= char <= '9':

         minus = (dig_shift1 - dig_shift2)

         base_num = ord ('0')

         pos5 = ord (char) - base_num

         new_pos5 = (pos5 + minus) %10

         return chr (new_pos5 + base_num)
   
    return char

#function for reverting all the shifts in the shiftfunction 

def reverse_shift (char, shift1, shift2, dig_shift1 = shift_num1, dig_shift2 = shift_num2):
         #Number reverse 0-9
         if '0' <= char <= '9':  #looks between the 0-9 to see whats in between them

          minus = dig_shift2 - dig_shift1  #creating the subtraction variable for the 2 shifts, but with reverting you can swap the 2 subtractions around to get a shiftback

          base_num = ord ('0')  #this sets the base or start num of the ord function to 0 

          pos5 = ord (char) - base_num #this does the ord for the program and computer to figure out for char - that base num

          new_pos5 = (pos5 + minus) %10 #calculates from the base num and current position of the text using the modulo %10 to represent the cycle and wrap around of 0-9

          return chr (new_pos5 + base_num) #returning the functions calculation of the chr then adding that new_pos (position) to the start or base num to get our shift
         #Lowercase reverse a-n            #the return also is in place to not allow discrepencies or issues in between the if statements 
         if 'a' <= char <= 'n':

               multiplier = shift1 * shift2 

               pos = ord(char) - ord ('a')

               new_pos = (pos - multiplier) % 14  #all reversion if statements are the same with different ways to convert back, here it is just flipped

               return chr (new_pos + ord('a'))    #from a + the multiplier to - the multiplier from the position 
         #lowercase reverse o-z
         if 'o' <= char <= 'z':

            pos2 =ord(char) - ord ('o')
         
            addition = shift1 + shift2
         
            new_pos2 = (pos2 + addition) %12   # same thing as the a-n block this one just subtracts the - letting the chr and ord do the work in reversion ***swapped the signs here also
         
            return chr(new_pos2 + ord('o'))
         #Uppercase reverse A-M
         if 'A' <= char <= 'M':
                      
                    pos3 = ord (char) - ord ('A') 
                      
                    new_pos3 = (pos3 + shift1) %13 #this has the + flipped from a - to do the reversion *** 14% to 13% to match the A-M range of letters
                      
                    return chr (new_pos3 + ord ('A'))
         #Uppercase reverse N-Z
         if 'N' <= char <= 'Z':
                 
                        pos4 = ord (char) - ord ('N')
         
                        squared = shift2 * shift2
                         
                        new_pos4 = (pos4 - squared) %13 #this one has the - also flipped from the + although can act up sometimes giving a letter discrepency
                 
                        return chr (new_pos4 + ord ('N'))
        
         return char
 

def process_file(input, output, shift1, shift2, dig_shift1 = shift_num1, dig_shift2 = shift_num2):  #this creates the processfile function having all our stored values in the parameter section 
    try:  #attempts the function then if it dosent work we get the filenowfounderror
        
        with open(input, 'r') as infile:  #this reads the inputfile aka the input.txt                    
            content = infile.read()       #stored as a content var to read the file for the shift to get its input to shift                           

        encrypted_content = ''.join(shift_function(c, shift1, shift2, dig_shift1, dig_shift2) for c in content)  #.join to the shiftfunction using all our shifts on the text in content (input.txt)

        with open(output, 'w') as outputfile:  #this will write to output file                
                  
            outputfile.write(encrypted_content)  #the actual function of writing to the output file and we are inputing our (encrypted content)   

            import time

            seconds = 3

            print(f'Encrypting text please standby !')

            while seconds > 0:

                time.sleep(1)

                seconds -= 1

            print(f'SUCCESS ! Encrypted content stored to : {output}') #just announces whether or not the shift was completed 

    except FileNotFoundError: #our file not found error
         
         print(f'ERROR >>> The file {input} was not found.')   #the print if the file was not found

process_file(file_path, file_path1 , shift_num1, shift_num2) #this uses our def function process_file all it does is assign the input and output txt files and the shift1 and 2 numbers from our user input *** Needed for absolute path to work properly with the input and output files.


def decrypt_file (output, decrypt, shift1, shift2, dig_shift1 = shift_num1, dig_shift2 = shift_num2): #likes our process file function the decrypt file does the exact same thing.
    try:
         with open (output, 'r') as infile:
              content = infile.read()

              decrypted_content = ''.join(reverse_shift(c, shift1, shift2, dig_shift1, dig_shift2) for c in content) #unlike the process file one we just have the reverse_shift function

              with open (decrypt, 'w') as decryptfile:
                   
                   decryptfile.write (decrypted_content)

                   import time #import the time module just for some extra flavour

                   seconds = 5 #var for loop counter

                   print(f'Decrypting the text, grab some popcorn :) ')

                   while seconds > 0: #while the seconds are greater it will count 
                        
                        time.sleep(1) 

                        seconds -= 1

                   print (f'SUCCESS ! Your encrypted content was stored to : {decrypt}')

    except FileNotFoundError:
         
         print (f'ERROR >>> The file output.txt was not found !') 

decrypt_file (file_path1, file_path2, shift_num1, shift_num2) #this just runs our decrypt_file function to input our decrypted content from our reverseshift function and put it into our decrypt file *** Needed for absolute path to work properly with the input and output files.


  
with open (file_path, 'r') as inputcheck, open (file_path2, 'r') as decryptcheck: # ***also changed for absolute path to work.
      
      if inputcheck.read() == decryptcheck.read(): #checking and comparing through == if the 2 .reads of each file are the same

        print('Your decryption text seems to be accurate, enjoy !')

      else:
            
            print ('Decryption was unsuccessful this time, maybe use some better numbers :( ? ')  


  


