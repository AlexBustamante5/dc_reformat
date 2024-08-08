# breaks a big marcxml file into smaller files based on a keyword

# python3 makefile.py input/books_100-200.xml non_dupes_records 

import os
import re
import argparse

def makefile(input_file, save_dir, keyword = '</record>'):
    # string used to split the content into individual records
    # '</record>' used to mark the end of an xml record

    os.makedirs(save_dir, exist_ok=True)

    #  opens the file in read mode with UTF-8 encoding, reads its content, and stores it in the variable content
    with open(input_file, 'r', encoding='utf-8') as f:        
        content = f.read()

    # splits the entire content string into a list of parts using the keyword (</record>) as the delimiter
    # each element in the parts list represents a record 
    parts = content.split(keyword)

    ## debug
    # print(parts)

    # loops over the parts list and provides and index for each part
    for i, part in enumerate(parts):

        # this strips the part of any whitespaces and if the result is not empty, it proceeds with the  next if block
        if part.strip():  
            if i < len(parts) - 1:
                # if the part is not the last one in the list, it appends the keyword to it
                part += keyword

            # searches the record for bib number and renames file as such
            # re.search uses a regular expression to search for a specific pattern within part 
            # the pattern looks for a datafield element with tag 999 and a subfield element with code c, capturing its content
            # the (.+?) is a non-greedy match for any content within the subfield element
            bib_match = re.search(r'<datafield tag="999" ind1=" " ind2=" ">\s*<subfield code="c">(.+?)</subfield>', part)

            # if bib_match is not None, it is extracted using bib_match.group(1)
            if bib_match:
                bib_number = bib_match.group(1)
            else:
                bib_number = f'unknown-{i + 1}'
            
            # constructs the output file
            output_file = os.path.join(save_dir, f'bib-{bib_number}.xml')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(part)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a big MARCXML file and split it into individual records.')
    parser.add_argument('input_file', help='Path to the input MARCXML file')
    parser.add_argument('save_dir', help='Directory to save the individual record files')
    args = parser.parse_args()

    makefile(args.input_file, args.save_dir)
