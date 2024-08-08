import os
import shutil
from pymarc import parse_xml_to_array
from pymarc.exceptions import FatalReaderError, RecordLeaderInvalid, NoFieldsFound, FieldNotFound

# 856z
### some records have duplicate info in other subfield of field 856

def find_dupes(source_folder, destination_folder, keyword):

    # ensures destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # iterates through files in source folder
    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)

        if not os.path.isfile(file_path):
            continue
    
        # checks if it is a dupe
        try:
            with open(file_path, 'rb') as file:
                reader = parse_xml_to_array(file)
                isDupe = False

                for record in reader:
                    for field in record.get_fields('856'):
                        for sub_field in field:
                            if keyword in sub_field.value:
                                isDupe = True
                                break
                        if isDupe:
                            break
                    if isDupe:
                        break
        except (FatalReaderError, RecordLeaderInvalid, NoFieldsFound, FieldNotFound, Exception) as e:
            print(f"Error processing file {file_path}: {e}")
            continue

        # move file if isDupe
        if isDupe:
            shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))

source_folder = # enter source folder path
destination_folder = # enter destination folder path
keyword = # enter keyword
find_dupes(source_folder, destination_folder, keyword)
