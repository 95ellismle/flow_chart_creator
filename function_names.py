"""

    A little program to print out which subroutines are in a piece of FORTRAN 
    code. 
    
    Can use flags, -b, -c and -i. -i is the input file to check for 
    SUBROUTINES. -b will also check for a description and print it out under
    the name of the subroutine. -c will print out the subroutines that are 
    called within a subroutine.
  
    An example of the use this program... 
      python3 <dir_of_code> -i example.F -bc

    Recommend adding an alias in your bashrc.

"""


# Add a flag to find functions and print them along with some stats etc...


import os

pwd = os.getcwd()

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-b", action="store_true", default=False, help="Turns off searching for a description to optimise performance")
parser.add_argument("-i", "--input", help="Name of the file to act upon")
parser.add_argument("-c", action='store_true', default=False, help="Prints the functions called within functions")

args = parser.parse_args()

if (args.input):
  file = pwd + '/' + args.input
else:
  file = "/scratch/mellis/flavoured-cptk/cp2k/src/aom_utils.F"

Otext = open(file).read()
text = Otext[:]

functions = []


filename_without_the_path = file[file.rfind('/') + 1:] 
print("\nThe functions in the file \"%s\" are:"%filename_without_the_path)

# Will find the description of the function if the \brief tag is used
def brief_finder(text, sub_name, end_statement="END SUBROUTINE"):
  i_max = text.find(sub_name)
  i_brief = text[:i_max].rfind("rief") + 4
  i_end_brief = i_brief + text[i_brief:i_max].find("!")
  brief = text[i_brief:i_end_brief].lstrip(' ')
  print("  Description: %s\n"%brief.strip())
  return brief

# A function to find certain bits of text
def statement_finder(text, counter, begin_statement="SUBROUTINE", end_statement="END SUBROUTINE", splice="(", name_of_statement="Statement"):
  if text.find(begin_statement) > 0: 
    i1 = text.find(begin_statement) + len(begin_statement)
    i2 = i1 + text[i1:].find(splice)
    i3 = i1 + text[i1:].find(end_statement) + len(end_statement)
    
    statement_text = text[i1:i3]
    function_name = text[i1:i2]
    text = text[i3:]
    print("%s %i:"%(name_of_statement, counter), "%s"%function_name.strip() )
    return text, statement_text, function_name
  return "",""



counter = 1
while (text.find("SUBROUTINE") > 0):
#for i in range(1):
  text,statement_text, fname = statement_finder(text, counter, name_of_statement="-Subroutine")
  if args.b:  
    brief_finder(Otext, fname)
  counter += 1
  Ccount = 1
  if args.c:
    while (statement_text.find("CALL") > 0):
      statement_text, _, cname = statement_finder( statement_text, 
                                           Ccount, 
                                           begin_statement="CALL ", 
                                           end_statement=")", 
                                           name_of_statement="\t*CALL")
      Ccount += 1

    print("") 
