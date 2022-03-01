"""
Course:        DCS 211 Winter 2022
Assignment:    Lab 1
Topic:         Python Review
Purpose:       Implement several different functions for Python review

Student Name: Kevin Chen
Partner Name: Sophie Alexis

Other students outside my pair that I received help from ('N/A' if none):
    ...

Other students outside my pair that I gave help to ('N/A' if none):
    ...

Citations/links of external references used ('N/A' if none):
    ...

"""

from typing import Callable
import time
import string
import typing


#####################################################
def countDown(n: int, duration: int | float) -> None:
    """ counts downward from n to 0, inclusive, only printing
    Parameters
        n: an integer corresponding to the upper limit for counting down
        duration: a numeric value corresponding to the time between prints
    Returns
        None
    """
    if type(duration) != float and type(duration) != int:
        duration = 0.1  # default value
    for i in range(n, -1, -1):
        print(f"i == {i}")
        time.sleep(duration)
    return    # no return value here!

#####################################
def countZeros( list_: list[int] ) -> int:  # note use of _ avoiding conflict w/ list class
    """ returns a count of 0s, integer or character, in the given list

    This function accepts a list containing elements of any type, and counts
    the number of elements that are either numeric 0 or character 0, returning
    that count.

    Parameters
        list_: a list containing elements of any type
    Returns
        an integer count of the number of numeric 0 or character '0' in the list
    """
    count = 0
    for i in range(len(list_)):
        if list_[i] == 0 or list_[i] == '0':
            count += 1
    return count

##########################
# For you to implement:
#   countDigits(string_: str ) -> int:
#       count & return the number of digits in the given string
#   extractDigits(string_: str) -> str:
#       return a string consisting only of the digits in the given string;
#       use a loop-based build-string-from-scratch approach
#   extractDigits2(string_: str) -> str:
#       return a string consisting only of the digits in the given string;
#       use a dictionary-based approach to map characters using the translate
#       method available in the str class
#   extractLetters(string_: str) -> str:
#       return an only-letters version of string, all converted to lowercase;
#       use a loop-based build-string-from-scratch approach
#   extractLetters2(string_: str) -> str:
#       return an only-letters version of string, all converted to lowercase;
#       use a dictionary-based approach to map characters using the translate
#       method available in the str class
#   readFile(filename: str) -> list[int, list[str]]:
#       Read the file with given filename, building and returning a list.
#       In the file:
#           - if the line begins with '-', convert to only-letters-lowercased;
#           - if the line begins with '#', convert to only-digits.
#       The list returned must contain two elements:
#           (1) the number of digits discarded in the process
#           (2) a list of strings, one string per line converted by the
#               specifications above.

#############################################################################
def countDigits(count_str):
    digits = 0
    valid_nums = string.digits
    for i in range(len(count_str)):
        if count_str[i] in valid_nums:
            digits += 1
    return digits

def extractDigits(ext_str):
    digits = ""
    valid_dig = string.digits
    for i in range(len(ext_str)):
        if ext_str[i] in valid_dig:
            digits += ext_str[i]
    return digits

def extractLetters(ext_str: str) -> str:
    """Function to extract an only-letters version of string, all converted to lowercase

    Args:
        ext_str (str): The input string.

    Returns:
        str: The extracted letters.
    """

    letters = ""
    valid_letters = string.ascii_letters
    for c in ext_str:
        if c in valid_letters:
            letters += c.lower()
    return letters

def extractDigits2(ext_str: str) -> str:
   """Function to extract a string consisting only of the digits in the given string

   Args:
       ext_str (str): The input string.

   Returns:
       str: The extracted digits.
   """

   uppercase_map = {i: None for i in range(65, 91)}
   lowercase_map = {i: None for i in range(97, 123)}
   digits = ext_str.translate({**uppercase_map, **lowercase_map})
   return digits

def extractLetters2(ext_str: str) -> str:
    """Function to extract an only-letters version of string, all converted to lowercase

    Args:
        ext_str (str): The input string.

    Returns:
        str: The extracted letters.
    """

    number_map = {i: None for i in range(48, 58)}
    letters = ext_str.translate(number_map)
    return letters.lower()

def readFile(filename): #-> list
  """Function: read the lines in a file and sort into new list of digits/letters and number of them
   Args: filename (name of file to be read)
   Returns: string_list (list of sorted digits/letters and number of rejected digits"""

   open_file = open(filename,"r")
   read_lines = open_file.readline().strip()
   string_list = []
   disc_digits = 0
   while read_lines != "":
       if read_lines[0] == "#":
           string_list.append(extractDigits(read_lines))
       if read_lines[0] == "-":
           string_list.append(extractLetters(read_lines))
           disc_digits += int(len(extractDigits(read_lines)))
       read_lines = open_file.readline()

   final_list = [disc_digits] + [string_list]
   return final_list

def testHarness(fcn: Callable, arg: str, expected: str | list) -> None:
    ''' function to help test an arbitrary function having one argument
    Parameters:
        fcn: the actual function being tested (pass without calling)
        arg: the argument being passed to the tested function
        expected: the expected result, either str or list in the context here
    Returns:
        None -- just prints
    '''
    result = fcn(arg)  # call the student's function, passing the given argument

    # see https://unicode-table.com/en/sets/check/
    # replace these as you see fit
    mark = "✓" if result == expected else "✗"
    if type(arg) == str:
        print(f"Testing {fcn.__name__}(\"{arg}\"):")
    else:
        print(f"Testing {fcn.__name__}({arg}):")
    print(f"\t {mark}result   = {result}")
    print(f"\t  expected = {expected}")

############################################################
# An example main() function - to keep everything organized!
#
def main() -> None:
    """ main function for organizing -- and printing -- everything """
    # sign on
    print(f"\n\n{'-' * 20} Start of main() {'-' * 20}\n\n")

    # testing countDown
    print("Testing countDown(10, 0.1):")
    countDown(10, 0.1)
    print()

    print("Testing countDown(10, 'x'):")
    countDown(5, "x")
    print()

    # testing countZeros
    aList = [8,0,8,8,0,0,8,0,8]
    expected = 4
    print(f"Testing countZeros({aList}):")
    print(f"\t result   = {countZeros(aList)}")
    print(f"\t expected = {expected}")

    aList = [8,'0',8,8,0,'0','8',0,8,'0',0]
    expected = 6
    print(f"Testing countZeros({aList}):")
    print(f"\t result   = {countZeros(aList)}")
    print(f"\t expected = {expected}")

    aList = []
    expected = 0
    print(f"Testing countZeros({aList}):")
    print(f"\t result   = {countZeros(aList)}")
    print(f"\t expected = {expected}")
    print()

    #testing countDigits
    print("Testing countDigits(12345678910):")
    print(countDigits(str(12345678910)))
    print("Expected = 11")

    print(f"Testing countDigits(1a3b5c78c11):")
    print(countDigits("1a3b5c78c11"))
    print("Expected = 7")

    print(f"Testing countDigits(abd12,kfdsjla1;): ")
    print(countDigits("abd12,kfdsjla1;"))
    print("Expected = 3")

    print(f"Testing countDigits(abcdefghij): ")
    print(countDigits("abcdefghij"))
    print("Expected = 0")

    #testing extractDigits
    print("Testing extractDigits(12345678910):")
    print(extractDigits(str(12345678910)))
    print("Expected = 12345678910")

    print(f"Testing extractDigits(1a3b5c78c11):")
    print(extractDigits("1a3b5c78c11"))
    print("Expected = 1357811")

    print(f"Testing extractDigits(abd12,kfdsjla1;): ")
    print(extractDigits("abd12,kfdsjla1;"))
    print("Expected = 121")

    print(f"Testing extractDigits(abcdefghij): ")
    print(extractDigits("abcdefghij"))
    print("Expected = ")

    #testing extractLetters
    s = "abcd12ef34G0H0"
    expected = "abcdefgh"
    print(f"Testing extractLetters({s})")
    print(f"\t result = {extractLetters(s)}")
    print(f"\t expected = {expected}")
    print()

    #testing extractDigits2
    expected = "123400"
    print(f"Testing extractDigits2({s})")
    print(f"\t result = {extractDigits2(s)}")
    print(f"\t expected = {expected}")
    print()

    #testing extractLetters2
    expected = "abcdefgh"
    print(f"Testing extractLetters2({s})")
    print(f"\t result   = {extractLetters2(s)}")
    print(f"\t expected = {expected}")
    print()

    #testing readFile
    print(f"Testing readFile(input_10.txt): ")
    print(readFile("input_10.txt"))
    print("Expected = [11, ['1', '6941', '428', 'ercaldsrrvgvwujy', '782', 'uhglghkldmihwyxhxiehbky', 'ulzfxl', 'vueh', '', 'csdff']]")

    print(f"Testing readFile(input_20.txt): ")
    print(readFile("input_20.txt"))
    print("Expected = [5, ['2206835', '3184', '9', '', '', 'dxsksmwmqqmcxwjbbjqai', 'hoankfnvipn', '52899', '9', '5', '8066', '09274', '', '', '40', '7576', '6', '', '', 'btsrpizluvcq']]")

    print(f"Testing readFile(input_100.txt): ")
    print(readFile("input_100.txt"))
    print("Expected = [84, ['61', 'noidqyzwhmxvkoostuycatktz', 'xccvp', 'tkqsnjgjpylechswdndrrjhiqt', 'a', 'cohbctvdvrprstsbkaotcyy', '9045', '69', 'zhnyrpibdl', '32', 'hzosqjazcza', '61', '698', '16951', 'irvhyqeunyu', 'cljqhfc', '6217', '04', '444', 'hm', 'jwsnvburmvhsjbhzprozazfeo', '6', 'vhjjqazeufhh', '1439', 'mndxjpxhrddff', '2', 'vbyvvzozjqcnnphz', '3', 'otskpxnkrxdenowxigjzrqba', 'usr', '0584', 'kbkzuivsvewssggocohkmzd', 'ulnzn', '7', '0745', '', 'pxhpojoacbdbyxcsrvd', '491', '250', '6', 'zsrwibtekpvesait', '3', '936', '0316', 'grlrlx', 'pibqewwpcgpkhrrxvu', 'ndlmb', 'mavjoxm', '', '', '96', '0355991', '83', '94', 'xzaajxdm', 'mwphrrhftxvxgswyrslwsmiraikm', '671', 'dwlumoqwefvyfwur', '9617', '7', '60', '32102', '4522', '', 'pmu', '', 'adtppwqrgljhuiyvpao', '', 'kv', '43', 'yfrtmjsnmi', 'xcrq', 'ntemaqmjjrjupokskb', 'ohwv', '369974', 'jxigo', 'i', 'vrccekspmtxgphxghonyyncrsx', '0', '84', 'obvevbizmrvjhxwbdaxumqnjsyb', 'zecej', '4', '', '2', '', '34855', '53', 'hgvajo', '', '7442', '38', '59', '', 'hheov', '655', 'aqoixrqpjypuhfey', '', 'xlcygessolntiqpfg', 'ealpberqgyfqxibcmxw']]")

    # function-naming sanity checks: just check whether the student's
    # functions are named correctly and accept correct number of arguments
    try:
        countDigits("")
        extractDigits("")
        extractDigits2("")
        extractLetters("")
        extractLetters2("")
        readFile("")
    except Exception as error:
        print(f"Function error: {error}")


    # the expected result for readFile("input_10.txt") will be:
    #   [11, ['1', '6941', '428', 'ercaldsrrvgvwujy', '782', 'uhglghkldmihwyxhxiehbky', 'ulzfxl', 'vueh', '', 'csdff']]

    # the expected result for readFile("input_20.txt") will be:
    #   [5, ['2206835', '3184', '9', '', '', 'dxsksmwmqqmcxwjbbjqai', 'hoankfnvipn', '52899', '9', '5', '8066', '09274', '', '', '40', '7576', '6', '', '', 'btsrpizluvcq']]

    # sign off
    print(f"\n\n{'-' * 20} End of main() {'-' * 20}\n\n")

# This conditional will run main() when this file is executed.
# However, this file can be imported in the interpreter and its function
# documentation queried, as in:
#       >>> from lab1.py import *
#       >>> help(countDown)
#       >>> help(countZeros)
#
if __name__ == "__main__":
    main()
