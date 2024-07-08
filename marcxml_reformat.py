import os
import xml.etree.ElementTree as ET
from pymarc import parse_xml_to_array
from xml.dom import minidom

def get_dc_fields(file_path):
    '''
    extracts dublin core fields from a MARC XML file
    takes in path to the MARC XML file
    returns a list of tuples containing dc tags and their values, and the identifier
    '''
    dc_fields = []
    
    with open(file_path, 'rb') as file:
        reader = parse_xml_to_array(file)
        for record in reader:
            for field in record.get_fields('245'):
                dc_fields.append(("dc:title", field['a']))

            for field in record.get_fields('100'):
                dc_fields.append(("dc:creator", field['a']))

            for field in record.get_fields('700'):
                subfield_a = field.get_subfields('a')
                for value in subfield_a:
                    dc_fields.append(("dc:creator", value))

            # HARD CODED
            ### RUN SQL TO GET ONLY BOOK TYPES 952c, 942c
                    
            dc_fields.append(("dc:type","Other"))

            for field in record.get_fields('260'):
                dc_fields.append(("dc:publisher", field['a']))

            for field in record.get_fields('260'):
                dc_fields.append(("dc:date", field['c']))

            for field in record.get_fields('505'):
                for subfield in field.get_subfields('a'):
                    dc_fields.append(("dc:description", subfield))

            for field in record.get_fields('650'):
                dc_fields.append(("dc:subject", field['a']))

            for field in record.get_fields('999'):
                if 'c' in field:
                    identifier = "https://ilob-olbi.juliencouturecentre.ca:8888/cgi-bin/koha/catalogue/detail.pl?biblionumber=" + field['c']
                    dc_fields.append(("dc:identifier", identifier))
    
    return dc_fields, identifier

def create_dc_tree(dc_fields, identifier):
    '''
    creates XML tree with dc fields
    takes:
        dc_fields (list)
        identifier (str)
    returns root element of the XML tree.
    '''
    # creates root
    root = ET.Element("record")

    # creates header sub elem
    header = ET.SubElement(root, "header")

    # creates id sub elem and adds id text
    id_elem = ET.SubElement(header, "identifier")
    id_elem.text = identifier

    # creates metadata subelem
    metadata = ET.SubElement(root, "metadata")

    # defines namespaces to avoid naming conflicts
    namespaces = {
    "xmlns:oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    "xmlns:dc": "http://purl.org/dc/elements/1.1/",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsi:schemaLocation": "http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
    }

    # adds namespaces to sub elem
    dc_elem = ET.SubElement(metadata, "oai_dc:dc", namespaces)

    # adds dc fields sub elems and texts
    for tag, value in dc_fields:
        field_element = ET.SubElement(dc_elem, tag)
        field_element.text = value
    
    return root

def write_pretty_xml(root, output_path):
    '''
    writes the XML tree to a file with pretty printing
    takes:
        root (Element)
        output_path (str)
    '''
    # ET.tostring serializes the root element and its children to a byte string using utf-8 encoding
    # .decode converts the byte string to a regular string
    xml_str = ET.tostring(root, encoding='utf-8').decode('utf-8')

    # minidom.parseString(xml_str) takes the XML string and parses it into a DOM structure
    # DOM structure: https://learn.microsoft.com/en-us/dotnet/standard/data/xml/xml-document-object-model-dom
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ", newl='\n', encoding=None)

    # remove the XML declaration
    pretty_xml_str = '\n'.join(pretty_xml_str.split('\n')[1:])

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml_str)

def reformat(input_path, output_path):

    dc_fields, identifier = get_dc_fields(input_path)
    root = create_dc_tree(dc_fields, identifier)
    write_pretty_xml(root, output_path)

def main():
    # paths
    input_folder = 
    output_folder = 

    os.makedirs(output_folder, exist_ok=True)
    
    for input_name in os.listdir(input_folder):
        if input_name.endswith('.xml'):
            output_name = input_name.replace('.xml', '_dc2.xml')
            output_path = os.path.join(output_folder, output_name)
            input_path = os.path.join(input_folder, input_name)

            try:
                reformat(input_path, output_path)
            except Exception as e:
                print(f"Error processing {input_name} : {e}")
                continue

if __name__ == "__main__":
    main()
