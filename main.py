"""
Phone number regex decison tree :



                                                                (?:\s+|)*  -->   whitespace characters
                                                                    |
                                                                    |
                                                                    |
                                                    ((0|(?:(\+|)91)|(?:\((\+|)91)\))   -->   prefixes : no character,0,+91,91,(+91)
                                                                    |
                                                                    |
                                                                    |
                                                                (?:\s|-)   -->  0 or 1 intermediate whitespace characters or dashes
                                                                    |
                                                                    |
                                                                    |
        -----------------------------------------------------------------------------------------------
        |                           |                                                                 |
 10 digit number              Mobile Number                                                   Landline Number
     \d{10}                         |                                                                 |
                            Different Patterns                                                   Different Patterns                
                      ------------------------------                            ----------------------------------------------------------
                      |                            |                            |                             |                          |
               3-3-4 digit code               2-3-5 digit code             2-8 digit code              3-7 digit code             4-6 digit code
            (starting with 7,8,9)           (starting with 7,8,9)               |                             |                          |
                      |                            |                  (?:\d{2}(?:\s|-)\d{8})      (?:\d{3}(?:\s|-)\d{7})   (?:\d{4}(?:\s|-)\d{6})
                      |                            |
(?:\d{3}(?:\s|-)\d{3}(?:\s|-)\d{9})   (?:\d{2}(?:\s|-)\d{3}(?:\s|-)\d{5})   
"""

import re
import os
import sys
import csv

L_SPACES = r'(?:\s+|)'
PHONE_PREFIXES = r'((0|(?:(\+|)91)|(?:\((\+|)91)\))'
I_SPACES = r'(?:\s|-)'
CODE_10 = r'\d{10}'
M_CODE_3_3_4 = r'(?:\d{3}(?:\s|-)\d{3}(?:\s|-)\d{9})'
M_CODE_2_3_5 = r'(?:\d{2}(?:\s|-)\d{3}(?:\s|-)\d{5})'
L_CODE_2_8 = r'(?:\d{2}(?:\s|-)\d{8})'
L_CODE_3_7 = r'(?:\d{3}(?:\s|-)\d{7})'
L_CODE_4_6 = r'(?:\d{4}(?:\s|-)\d{6})'

PHONE_REGEX_STR = L_SPACES+r'('+PHONE_PREFIXES+I_SPACES
PHONE_REGEX_STR += CODE_10+r'|'+M_CODE_3_3_4+r'|'+M_CODE_2_3_5+r'|'
PHONE_REGEX_STR += L_CODE_2_8+r'|'+L_CODE_3_7+r'|'+L_CODE_4_6+r')'
PHONE_REGEX_STR += L_SPACES

DEFAULT_PHONE_REGEX = re.compile(PHONE_REGEX_STR)

def scan_dir(root_dir, csv_writer, phone_regex=DEFAULT_PHONE_REGEX):
    """
    Recursively traverse the root_dir and scan each text file for phone numbers. Then
    save the extracted phone numbers in a csv file.

    Assumptions
    -----------

        1. A text file has .txt extension
        2. There are no soft links or symlinks, therefore no file system loops will
           be encountered while recursive traversal
    """

def extract_phone_no(file_name, phone_regex):
    """
    Examples of phone numbers :

    Mobile numbers :

    7,8,9

    +917036141002
    +91 7036141002
    +91-7036141002
    +91 7036141002
    917036141002
    91 7036141002
    7036141002
    07036141002
    0 7036141002
    0-7036141002
    70361 41002
    070361 41002
    0 70361 41002
    70 361 41002
    070 361 41002
    070-361-41002
    0 70 361 41002
    (+91)7036141002


    Landline numbers :

    022-24130000 
    080 25478965
    0-80-25478965
    0416-2565478 
    08172-268032 
    04512-895612 
    0-4512-895612
    02162-240000 
    022-24141414 
    079-22892350

    +91 80 25478965
    +91 416 2565478
    +91 8172 268032

    +91-80-25478965
    +91-0416-2565478
    +91-8172-268032

    (+91)8025478965
    """
