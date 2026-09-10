
from pathlib import Path #this is the inbuilt python function to find files easier 

project_path = Path(__file__).parent   #Sets the variable project_path as Path file and then .parent to get the parent directory of the file
absolute_project_path = project_path.resolve() #This sets the variable absolute_project_path as project_path and then .resolve to get the absolute path of the file


file_path = project_path / 'raw_text.txt'   #the raw_text.txt file is stored in the variable file_path using the project_path variable and then / to get the file name
file_path1 = project_path / 'encrypted_text.txt' #the encrypted_text.txt file is stored in the variable file_path1 using the project_path variable and then / to get the file name
file_path2 = project_path / 'decryption_text.txt' #the decryption_text.txt file is stored in the variable file_path2 using the project_path variable and then / to get the file name





for attempt in range (5): #to prompt the user to enter correct inputs that are an int not anything else

    try:                  #to try this and give a value error if inccorect (not a number) and then prompt the user to try again until they get it right or run out of attempts
          
          shift_num1 = int (input (f'You have 5 attempts, this is {attempt + 1}/5 enter a valid number for shift value 1 :\n'))

          break #if (true) and the value is correct
    
    except ValueError:
          
          print ('That is not a valid number, please try again !')
else : 

      print ('All attempts used up please try again later !')

      exit ()
            



for attempt in range (5): #to prompt the user to enter correct inputs that are an int not anything else

    try:                  #to try this and give a value error if inccorect (not a number) and then prompt the user to try again until they get it right or run out of attempts
           
          shift_num2 = int (input (f'You have 5 attempts, this is {attempt + 1}/5 enter a valid number for shift value 2 :\n')) #to prompt the user to enter a valid number for the second shift
          break #if (true) and the value is correct
    
    except ValueError:  #if the inputted value generates an error since the input is a int if a non digit is entered it will cause the error
          
          print ('That is not a valid number, please try again !')

else :

      print ('All attempts used up please try again later !')

      exit ()




        
  
#the function that does all the shifting and assigns the shift1/2 and dig_shift1/2 the user inputted values later in the program (same for reverse_shift)


def shift_function (char, shift1, shift2, dig_shift1 = shift_num1, dig_shift2 = shift_num2): #this is the shift_function block which does all the sorting and character shifting
    
    #Lowercase a-n shift

    if 'a' <= char <= 'n':         #each one is the same structure with a different shifting movement assigned for each range of letters capitals or numbers ect for all the if statements through the shift_function block

        pos_1 = ord(char) - ord ('a')  #starts the ord of char at 'a'

        multiplier = shift1 * shift2  #multiplies the 2 shift functions

        new_pos_1 = (pos_1 - multiplier) % 14 #prevents the text from going over 14 letters and wraps it back around to its numerical start point within letters between a-n also adds our position to our multiplier under the new_pos
                                          #^^ is the modulo operator which is used to wrap around the alphabet and keep the shifted position within the range of a-n
        return chr (new_pos_1 + ord('a'))   #returns the new position of the shifted character by converting it back to a character using chr and adding the new position to the ord of 'a' to get the correct shifted character
    
    #Lowercase o-z shift

    if 'o' <= char <= 'z':

        pos_2 =ord(char) - ord ('o')

        addition = shift1 + shift2

        new_pos_2 = (pos_2 + addition) %12

        return chr(new_pos_2 + ord('o'))
    
    #capital A-M shift

    if 'A' <= char <= 'M':
    
            pos_3 = ord (char) - ord ('A')
    
            new_pos_3 = (pos_3 + shift1) %13
    
            return chr (new_pos_3 + ord ('A'))
    
    #capital N-Z shift

    if 'N' <= char <= 'Z':
        
                pos_4 = ord (char) - ord ('N')

                shift_squared = shift2 * shift2
                
                new_pos_4 = (pos_4 - shift_squared) %13
        
                return chr (new_pos_4 + ord ('N'))
    
    #Number shift 0-9

    if '0' <= char <= '9':

         shift_minus = (dig_shift1 - dig_shift2)

         base_num = ord ('0')

         pos_5 = ord (char) - base_num

         new_pos_5 = (pos_5 - shift_minus) %10

         return chr (new_pos_5 + base_num)
   
    return char


#decryption back from the encrypted text

def reverse_shift (char, shift1, shift2, dig_shift1 = shift_num1, dig_shift2 = shift_num2): #function for reverting all the shifts in the shiftfunction 
         
         #Number reverse 0-9

         if '0' <= char <= '9':  #looks between the 0-9 to see whats in between them

          shift_minus = dig_shift2 - dig_shift1  #creating the subtraction variable for the 2 shifts, but with reverting you can swap the 2 subtractions around to get a shiftback

          base_num = ord ('0')  #this sets the base or start num of the ord function to 0 

          pos_5 = ord (char) - base_num #this does the ord for the program and computer to figure out for char - that base num

          new_pos_5 = (pos_5 - shift_minus) %10 #calculates from the base num and current position of the text using the modulo %10 to represent the cycle and wrap around of 0-9

          return chr (new_pos_5 + base_num) #returning the functions calculation of the chr then adding that new_pos (position) to the start or base num to get our shift
         
         #Lowercase reverse a-n            #the return is to convert the new pos back to characters using our chr and doing new_pos + base num to get the correct shifted character

         if 'a' <= char <= 'n':

               shift_multiplier = shift1 * shift2 

               pos_1 = ord(char) - ord ('a')

               new_pos_1 = (pos_1 + shift_multiplier) % 14  #all reversion if statements are the same with different ways to convert back, here it is just flipping the + to a - to get the reversion of the shift and then using the modulo to wrap around the alphabet and keep the shifted position within the range of a-n

               return chr (new_pos_1 + ord('a'))    
         
         #lowercase reverse o-z

         if 'o' <= char <= 'z':

            pos_2 =ord(char) - ord ('o')
         
            shift_addition = shift1 + shift2
         
            new_pos_2 = (pos_2 - shift_addition) %12   # same thing as the a-n block this one just subtracts the - letting the chr and ord do the work swapping the values back to a character and so on
         
            return chr(new_pos_2 + ord('o'))
         
         #Uppercase reverse A-M

         if 'A' <= char <= 'M':
                      
                    pos_3 = ord (char) - ord ('A') 
                      
                    new_pos_3 = (pos_3 - shift1) %13 #this has the + flipped from a - to do the reversion 
                      
                    return chr (new_pos_3 + ord ('A'))
         
         #Uppercase reverse N-Z

         if 'N' <= char <= 'Z':
                 
                        pos_4 = ord (char) - ord ('N')
         
                        shift_squared = shift2 * shift2
                         
                        new_pos_4 = (pos_4 + shift_squared) %13 #this one has the - also flipped from the + although can be incorrect sometimes giving a letter discrepency for decryption (only with some shift values though)
                 
                        return chr (new_pos_4 + ord ('N'))
        
         return char


 

def process_file(input, output, shift1, shift2, dig_shift1 = shift_num1, dig_shift2 = shift_num2):  #this creates the processfile function with our input as raw_text the output as encrypted_text shift1/2 as the inputted values and dig_shift1/2 as the inputted values for the numbers in the text

    try:  #attempts the function then if it dosent work we get the filenowfounderror
        
        with open(input, 'r') as infile:  #this reads the raw_text.txt file and stores it as infile to be used in the next line           

            content = infile.read()       #stored as a content var to read the file for the shift to get its input to shift                           

        encrypted_content = ''.join(shift_function(c, shift1, shift2, dig_shift1, dig_shift2) for c in content)  #here the .join is used to join the shifted characters together into a single string and then we use the shift_function to shift each character in the content using the provided shift values

        with open(output, 'w') as outputfile:  #this will write to encryped_text.txt file                
                  
            outputfile.write(encrypted_content)  #the actual function of writing to the output file and we are inputing our (encrypted content)   

            import time #This is for visual pleasement and to give the user a sense of time passing while the encryption is happening, just for fun and to make it feel more like a process

            seconds = 3 #this is the var for the loop counter to count down from 3 seconds

            print(f'Encrypting text please standby !\n') #prints a message to the user indicating that the text is being encrypted

            while seconds > 0: #while the seconds are greater it will count down and then print a message to the user indicating that the text is being encrypted

                time.sleep(1) #sleep increment of 1 second with our set seconds at 3 

                seconds -= 1 #this just decrements the seconds by 1 each time the loop runs until it reaches 0 and then exits the loop

            print(f'SUCCESS ! Encrypted content stored to : {output}\n') #just announces whether or not the shift was completed 

    except FileNotFoundError: #our file not found error
         
         print(f'ERROR >>> The file {input} was not found.\n')   #the print if the file was not found

process_file('raw_text.txt' , 'encrypted_text.txt', shift_num1, shift_num2) #this uses our def function process_file all it does is assign the raw and encrypted txt files and the shift1 and 2 numbers from our user input




def decrypt_file (output, decrypt, shift1, shift2, dig_shift1 = shift_num1, dig_shift2 = shift_num2): #like our process file function the decrypt file does the exact same thing.
    try:
         with open (output, 'r') as infile:
              content = infile.read()

              decrypted_content = ''.join(reverse_shift(c, shift1, shift2, dig_shift1, dig_shift2) for c in content) #unlike the process file one we just have the reverse_shift function

              with open (decrypt, 'w') as decryptfile:
                   
                   decryptfile.write (decrypted_content)

                   import time #This is for visual pleasement and to give the user a sense of time passing while the decryption is happening, just for fun and to make it feel more like a process

                   seconds = 5 #var for loop counter

                   print(f'Decrypting the text, grab some popcorn :)\n')

                   while seconds > 0: #while the seconds are greater it will count until it reaches 0 and then exits the loop
                        
                        time.sleep(1)  #sleep increment of 1 second with our set seconds at 5

                        seconds -= 1

                   print (f'SUCCESS ! Your encrypted content was stored to : {decrypt}\n')



    except FileNotFoundError: #our file not found error
         
         print (f'ERROR >>> The file output.txt was not found !\n')   #the print if the file was not found

decrypt_file ('encrypted_text.txt' , 'decryption_text.txt', shift_num1, shift_num2) #this just runs our decrypt_file function to input our decrypted content from our reverseshift function and put it into our decrypt file




  
with open ('raw_text.txt' , 'r') as inputcheck, open ('decryption_text.txt', 'r') as decryptcheck:
      
      if inputcheck.read() == decryptcheck.read(): #checking and comparing through == if the 2 .reads of each file are the same

        print('Your decryption text seems to be accurate, enjoy !\n')

      else:
            
            print ('Decryption was unsuccessful this time, maybe use some different / better numbers :( ?\n ')  #this is in place for the case of the raw_text and decrypt_text not being == so just a message to tell the user is was unsuccessful due to the shift values provided

