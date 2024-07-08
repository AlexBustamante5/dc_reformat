from pymarc import parse_xml_to_array

# reads a marcxml file

def main(file):
    try:
        # checks if record is empty - if not, prints record fields
        with open(file, 'rb') as fh:
            reader = parse_xml_to_array(fh)
            for record in reader:
                if record is not None:
                    print("Full record")
                    read(record)
                else:
                    print("Empty record encountered")
    except FileNotFoundError:
        print(f"Error: {file} not found.")
    except Exception as e:
        print(f"Error: {e}")

def read(record):

    #title
    title_a = record['245']['a']
    title_b = record['245']['b'] if record['245'] and 'b' in record['245'] else ' '
    title = title_a + title_b
    print(f'title: {title}')

    #creator
    creator = record['100']['a']
    print(f'creator: {creator}')

    #additional creators
    for field in record.get_fields('700'):
        for subfield_a in field.get_subfields('a'):
            print(f'additional creators: {subfield_a}')

    #publisher
    publisher = record['260']['a'] + record['260']['b']
    print(f'publisher: {publisher}')

    #date
    date = record['260']['c']
    print(f'date: {date}')

    #description
    for f in record.get_fields('505'):
        subfield_a = f.get_subfields('a')
        for value in subfield_a:
            print(f'description: {value}')

    #subject
    for f in record.get_fields('650'):
        subfield_a = f.get_subfields('a')
        for value in subfield_a:
            print(f'subject: {value}')
#file path
file = 
main(file)
