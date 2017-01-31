"""
Phone number regex decison tree
-------------------------------
```



                                                            (?:(?<=\s)|(?<=^))  -->   whitespace characters
                                                                    |
                                                                    |
                                                                    |
                                                    (0|(?:(\+|)91)|(?:\((\+|)91)\)|)   -->   prefixes : no prefix,0,+91,91,(+91)
                                                                    |
                                                                    |
                                                                    |
                                                                (?:\s|\-|)   -->  0 or 1 intermediate whitespace characters or dashes
                                                                    |
                                                                    |
                                                                    |
        ----------------------------------------------------------------------------------------------------------------------------------------------
        |                                    |                                                                                                       |
 10 digit number                       Mobile Number                                                                                         Landline Number
     \d{10}                                  |                                                                                                       |
                                     Different Patterns                                                                                     Different Patterns
                      ----------------------------------------------------------------------                            ----------------------------------------------------------
                      |                                    |                               |                           |                             |                          |
               3-3-4 digit code                     2-3-5 digit code                5-5 digit code               2-8 digit code              3-7 digit code             4-6 digit code
            (starting with 7,8,9)                 (starting with 7,8,9)        (starting with 7,8,9)                   |                             |                          |
                      |                                    |                               |                    (?:\d{2}(?:\s|\-|)\d{8})      (?:\d{3}(?:\s|\-|)\d{7})   (?:\d{4}(?:\s|\-|)\d{6})
                      |                                    |                               |
(?:[789]\d{2}(?:\s|\-|)\d{3}(?:\s|\-|)\d{9}) (?:[789]\d{1}(?:\s|\-|)\d{3}(?:\s|\-|)\d{5})  |
                                                                                           |
                                                                              (?:[789]\d{4}(?:\s|\-|)\d{5})
```

Explanations for different patterns :

Mobile Numbers
--------------

 1. 3-3-4 digit code : Used for remembering mobile numbers
 2. 2-3-5 digit code : Based on 2-digit access code, 3-digit mobile switch code, 5-digit local subscriber code
 3. 5-5 digit code   : Generally used to represent phone numbers in Android phones

Landline Numbers
----------------

 1. 2-8 digit code : 2 digit STD code, 8 digit local subscriber code
 2. 3-7 digit code : 3 digit STD code, 7 digit local subscriber code
 3. 4-6 digit code : 4 digit STD code, 6 digit local subscriber code
"""

import re
import os
import csv
import argparse

# Checks for leading whitespace characters or start of string
START_SPACES = r'(?:(?<=\s)|(?<=^))'
# Checks for possible phone prefixes
PHONE_PREFIXES = r'(0|(?:(\+|)91)|(?:\((\+|)91)\)|)'
# Checks for intermediate space or dash
I_SPACES = r'(?:\s|\-|)'
# Checks for simple 10 digit number
CODE_10 = r'\d{10}'
# Checks for mobile numbers written in pattern of 3-3-4 digits
M_CODE_3_3_4 = r'(?:[789]\d{2}(?:\s|\-|)\d{3}(?:\s|\-|)\d{9})'
# Checks for mobile numbers written in pattern of 2-3-5 digits
M_CODE_2_3_5 = r'(?:[789]\d{1}(?:\s|\-|)\d{3}(?:\s|\-|)\d{5})'
# Checks for mobile numbers written in pattern of 5-5 digits
M_CODE_5_5 = r'(?:[789]\d{4}(?:\s|\-|)\d{5})'
# Checks for landline numbers written in pattern of 2-8 digits
L_CODE_2_8 = r'(?:\d{2}(?:\s|\-|)\d{8})'
# Checks for landline numbers written in pattern of 3-7 digits
L_CODE_3_7 = r'(?:\d{3}(?:\s|\-|)\d{7})'
# Checks for landline numbers written in pattern of 4-6 digits
L_CODE_4_6 = r'(?:\d{4}(?:\s|\-|)\d{6})'
# Checks for trailing whitespaces or end of string
END_SPACES = r'(?:$|\s+)'

PHONE_REGEX_STR = START_SPACES+r'('+PHONE_PREFIXES+I_SPACES+r'(?:'
PHONE_REGEX_STR += CODE_10+r'|'+M_CODE_3_3_4+r'|'+M_CODE_2_3_5+r'|'+M_CODE_5_5
PHONE_REGEX_STR += r'|'+L_CODE_2_8+r'|'+L_CODE_3_7+r'|'+L_CODE_4_6+r'))'
PHONE_REGEX_STR += END_SPACES

DEFAULT_PHONE_REGEX = re.compile(PHONE_REGEX_STR)
DEFAULT_FILE_EXT = '.txt'

def scan_dir(root_dir, file_ext=DEFAULT_FILE_EXT, phone_regex=DEFAULT_PHONE_REGEX):
    """
    Recursively traverse the root_dir and scan each text file for
    phone numbers. Then save the extracted phone numbers in a csv file.

    Assumptions
    -----------

        1. A text file has .txt extension otherwise the given extension
        2. There are no soft links or symlinks, therefore no file system
           loops will be encountered while recursive traversal
        3. os.walk() is intentionally not used in order to write the
           recursive function on my own
    """

    for file in os.listdir(root_dir):

        file_name = os.path.join(root_dir, file)

        # If file_name is subdirectory
        if os.path.isdir(file_name):
            yield from scan_dir(
                file_name,
                file_ext=file_ext,
                phone_regex=phone_regex)

        # Else if file_name is a text file
        elif file_name.endswith(file_ext):
            yield from extract_phone_no(file_name, phone_regex)


def extract_phone_no(file_name, phone_regex):
    """
    Extracts the phone number from file
    """

    with open(file_name) as fin:
        for ph_numbers in phone_regex.findall(fin.read()):
            yield ph_numbers[0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "targetdir",
        help="Root directory from where phone numbers are to be extracted")
    parser.add_argument(
        "--outputcsvfile",
        help="Destination file for saving phone numbers")
    parser.add_argument(
        "--file_extension",
        help="Extension of text files. Eg : txt, doc, csv")

    args = parser.parse_args()

    if args.outputcsvfile:
        with open(args.outputcsvfile,"w") as wt:
            contact_writer = csv.writer(wt)
            if args.file_extension:
                for ph_number in scan_dir(
                                    args.targetdir,
                                    file_ext='.'+args.file_extension):
                    contact_writer.writerow([ph_number])
            else:
                for ph_number in scan_dir(args.targetdir):
                    contact_writer.writerow([ph_number])
    else:
        if args.file_extension:
            for ph_numbers in scan_dir(
                                args.targetdir,
                                file_ext='.'+args.file_extension):
                print(ph_numbers)
        else:
            for ph_numbers in scan_dir(args.targetdir):
                print(ph_numbers)

if __name__ == "__main__":
    main()
