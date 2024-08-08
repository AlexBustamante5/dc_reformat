import os
from pymarc import parse_xml_to_array

def dupe_info(file_path, dupe_info_file):

    try:
        with open(file_path, 'rb') as file: # opens in binary mode
            reader = parse_xml_to_array(file)
            with open(dupe_info_file, 'a') as f:
                for record in reader:
                    f.write(file_path.split('/')[-1] + '\n')
                    for field in record.get_fields('856'):
                        for sub_field in field:
                            f.write('\t' + sub_field.code + ': ' + sub_field.value + '\n')           
    except Exception as e:
        print(f"Error {file_path} : {e}")
    return

def main(input_folder):
    dupe_info_file = # enter file path
    file_count = 0

    for input_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, input_name)
        try:
            dupe_info(input_path, dupe_info_file)
            file_count += 1
        except Exception as e:
            print(f"Error with {input_name}: {e}")
            continue

    with open(dupe_info_file, 'a') as f:
        f.write("Total number of files processed: " + str(file_count))

main(# enter folder path)
