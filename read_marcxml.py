from pymarc import parse_xml_to_array

# reads a marcxml file

file = # file path

# checks if record is empty - if not, prints record fields
with open(file, 'rb') as fh:
    reader = parse_xml_to_array(fh)
    for record in reader:
        if record is not None:
            print("Full record")
        else:
            print("Empty record encountered")
    
for record in reader:
    #title
    print ('title: ' + record['245']['a'])

    #creator
    print ('creator: ' + record['100']['a'])

    #additional creators
    for f in record.get_fields('700'):
        subfield_a = f.get_subfields('a')
        for value in subfield_a:
            print('additional creators: ' + value)

    #publisher
    print ('publisher: ' + record['260']['a'] + record['260']['b'])

    #date
    print ('date: ' + record['260']['c'])

    #description
    for f in record.get_fields('505'):
        subfield_a = f.get_subfields('a')
        for value in subfield_a:
            print('description: ' + value)

    #subject
    for f in record.get_fields('650'):
        subfield_a = f.get_subfields('a')
        for value in subfield_a:
            print('subject: ' + value)

    # duplicate info
    keyword = 'uOttawa'
    for field in record.get_fields('856'):
        for sub_field in field:
            if keyword in sub_field.value:
                print(sub_field.value)
