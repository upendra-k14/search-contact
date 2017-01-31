# search-contact
Recursively searches the contact numbers in text files in a given directory

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
(?:[789]\d{2}(?:\s|\-|)\d{3}(?:\s|\-|)\d{9})   (?:\d{2}(?:\s|-)\d{3}(?:\s|-)\d{5})   (?:[789]\d{4}(?:\s|\-|)\d{5})
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
 
Usage
-----

`python3 main.py [-h] targetdir [--outputcsvfile OUTPUTCSVFILE] [--file_extension FILE_EXTENSION]`

  Positional Arguments
  ---------------------

    targetdir             Root directory from where phone numbers are to be
                          extracted

  Optional Arguments
  -------------------
  
    -h, --help            show this help message and exit
  
    --outputcsvfile OUTPUTCSVFILE
                        Destination file for saving phone numbers
                        
    --file_extension FILE_EXTENSION
                        Extension of text files. Eg : txt, doc, csv

